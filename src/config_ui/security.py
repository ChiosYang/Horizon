"""Security boundary for the loopback-only configuration editor."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
import secrets
import threading
import time
from urllib.parse import urlsplit

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response


LOGGER = logging.getLogger("horizon.config_ui")

SESSION_COOKIE_NAME = "horizon_config_session"
CSRF_HEADER_NAME = "X-CSRF-Token"
BOOTSTRAP_PATH = "/api/v1/session/bootstrap"
API_PREFIX = "/api/v1/"
ALLOWED_HOSTNAMES = frozenset({"localhost", "127.0.0.1", "::1"})
SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})

CONTENT_SECURITY_POLICY = "; ".join(
    (
        "default-src 'none'",
        "script-src 'self'",
        "style-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    )
)


@dataclass(frozen=True, repr=False)
class LocalSession:
    """An authenticated browser session held only in process memory."""

    session_id: str = field(repr=False)
    csrf_token: str = field(repr=False)


class SessionStore:
    """Single-use bootstrap state and process-local authenticated sessions."""

    def __init__(self, bootstrap_token: str | None = None) -> None:
        self._bootstrap_token = bootstrap_token or secrets.token_urlsafe(32)
        self._sessions: dict[str, LocalSession] = {}
        self._lock = threading.Lock()

    @property
    def bootstrap_token(self) -> str | None:
        """Return the startup token while it remains usable."""

        with self._lock:
            return self._bootstrap_token

    def consume_bootstrap(self, candidate: str) -> LocalSession | None:
        """Consume the startup token exactly once and create a local session."""

        with self._lock:
            expected = self._bootstrap_token
            if expected is None or not secrets.compare_digest(candidate, expected):
                return None

            self._bootstrap_token = None
            session = LocalSession(
                session_id=secrets.token_urlsafe(32),
                csrf_token=secrets.token_urlsafe(32),
            )
            self._sessions[session.session_id] = session
            return session

    def get(self, session_id: str | None) -> LocalSession | None:
        """Look up a session without disclosing why authentication failed."""

        if not session_id:
            return None
        with self._lock:
            return self._sessions.get(session_id)


def _has_allowed_authority(value: str) -> bool:
    if not value or value != value.strip():
        return False
    try:
        parsed = urlsplit(f"//{value}")
        port = parsed.port
    except ValueError:
        return False

    return (
        parsed.hostname is not None
        and parsed.hostname.lower() in ALLOWED_HOSTNAMES
        and parsed.username is None
        and parsed.password is None
        and parsed.path == ""
        and parsed.query == ""
        and parsed.fragment == ""
        and (port is None or 1 <= port <= 65535)
    )


def host_header_is_allowed(value: str | None) -> bool:
    """Accept only exact loopback hostnames, with an optional valid port."""

    return value is not None and _has_allowed_authority(value)


def origin_is_allowed(value: str | None) -> bool:
    """Require a syntactically complete HTTP loopback origin."""

    if not value or value != value.strip():
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return False

    return (
        parsed.scheme.lower() == "http"
        and parsed.hostname is not None
        and parsed.hostname.lower() in ALLOWED_HOSTNAMES
        and parsed.username is None
        and parsed.password is None
        and parsed.path == ""
        and parsed.query == ""
        and parsed.fragment == ""
        and (port is None or 1 <= port <= 65535)
    )


def error_response(
    status_code: int,
    code: str,
    message: str,
    request_id: str,
) -> JSONResponse:
    """Create a stable error envelope without echoing rejected input."""

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
            }
        },
    )


class LocalSecurityMiddleware(BaseHTTPMiddleware):
    """Enforce the editor's Host, Origin, session, CSRF, and logging policy."""

    def __init__(self, app: object, *, session_store: SessionStore) -> None:
        super().__init__(app)
        self._sessions = session_store

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = secrets.token_hex(16)
        request.state.request_id = request_id
        started = time.perf_counter()

        try:
            response = await self._authorize_or_dispatch(request, call_next, request_id)
        except Exception:
            # Never include the exception or request data in logs or the response.
            response = error_response(
                500,
                "internal_error",
                "The local editor could not complete the request.",
                request_id,
            )
            LOGGER.error(
                "request_failed method=%s route=%s status=500 request_id=%s",
                request.method,
                self._route_template(request),
                request_id,
            )

        self._apply_security_headers(response, request_id)
        duration_ms = (time.perf_counter() - started) * 1000
        LOGGER.info(
            "request_complete method=%s route=%s status=%s duration_ms=%.2f request_id=%s",
            request.method,
            self._route_template(request),
            response.status_code,
            duration_ms,
            request_id,
        )
        return response

    async def _authorize_or_dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
        request_id: str,
    ) -> Response:
        if not host_header_is_allowed(request.headers.get("host")):
            return error_response(
                400,
                "invalid_host",
                "The request Host is not allowed.",
                request_id,
            )

        path = request.url.path
        is_state_changing = request.method.upper() not in SAFE_METHODS
        if is_state_changing and not origin_is_allowed(request.headers.get("origin")):
            return error_response(
                403,
                "invalid_origin",
                "A loopback Origin is required.",
                request_id,
            )

        bootstrap_request = (
            request.method.upper() == "POST" and path == BOOTSTRAP_PATH
        )
        requires_session = (
            (path.startswith(API_PREFIX) and not bootstrap_request)
            or (is_state_changing and not bootstrap_request)
        )

        session = None
        if requires_session:
            session = self._sessions.get(request.cookies.get(SESSION_COOKIE_NAME))
            if session is None:
                return error_response(
                    401,
                    "invalid_session",
                    "A valid local editor session is required.",
                    request_id,
                )
            request.state.session = session

        if is_state_changing and not bootstrap_request:
            candidate = request.headers.get(CSRF_HEADER_NAME)
            if candidate is None or session is None or not secrets.compare_digest(
                candidate,
                session.csrf_token,
            ):
                return error_response(
                    403,
                    "invalid_csrf",
                    "A valid CSRF token is required.",
                    request_id,
                )

        return await call_next(request)

    @staticmethod
    def _route_template(request: Request) -> str:
        route = request.scope.get("route")
        template = getattr(route, "path", None)
        return template if isinstance(template, str) else "<unmatched>"

    @staticmethod
    def _apply_security_headers(response: Response, request_id: str) -> None:
        response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
        )
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Request-ID"] = request_id
