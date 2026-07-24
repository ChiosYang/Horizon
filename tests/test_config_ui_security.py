from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import pytest

from src.config_ui.app import create_app
from src.config_ui.security import (
    CONTENT_SECURITY_POLICY,
    SESSION_COOKIE_NAME,
    SessionStore,
    host_header_is_allowed,
    origin_is_allowed,
)


BASE_URL = "http://127.0.0.1:8765"
LOOPBACK_ORIGIN = BASE_URL


def _client(app: FastAPI, **kwargs: object) -> TestClient:
    return TestClient(app, base_url=BASE_URL, **kwargs)


def _bootstrap(client: TestClient, token: str) -> str:
    response = client.post(
        "/api/v1/session/bootstrap",
        headers={"Origin": LOOPBACK_ORIGIN},
        json={"token": token},
    )
    assert response.status_code == 200
    return response.json()["csrf_token"]


@pytest.mark.parametrize(
    "host",
    [
        "localhost",
        "localhost:8765",
        "127.0.0.1",
        "127.0.0.1:8765",
        "[::1]",
        "[::1]:8765",
    ],
)
def test_host_allowlist_accepts_exact_loopback_authorities(host: str):
    assert host_header_is_allowed(host)


@pytest.mark.parametrize(
    "host",
    [
        None,
        "",
        "example.com",
        "localhost.example.com",
        "localhost.",
        "127.0.0.1.example.com",
        "127.0.0.1@evil.example",
        "::1",
        "[::1].example.com",
        "localhost:0",
        "localhost:65536",
        " localhost",
        "localhost/path",
    ],
)
def test_host_allowlist_rejects_non_loopback_or_malformed_values(host: str | None):
    assert not host_header_is_allowed(host)


@pytest.mark.parametrize(
    "origin",
    [
        "http://localhost",
        "http://localhost:8765",
        "http://127.0.0.1:8765",
        "http://[::1]:8765",
    ],
)
def test_origin_allowlist_accepts_http_loopback_origins(origin: str):
    assert origin_is_allowed(origin)


@pytest.mark.parametrize(
    "origin",
    [
        None,
        "",
        "null",
        "https://127.0.0.1:8765",
        "http://example.com",
        "http://localhost.example.com",
        "http://localhost:8765/path",
        "http://localhost:8765?token=secret",
        "http://user@localhost:8765",
        " http://localhost:8765",
    ],
)
def test_origin_allowlist_rejects_unsafe_values(origin: str | None):
    assert not origin_is_allowed(origin)


def test_public_shell_and_health_never_expose_config_or_bootstrap_data(tmp_path: Path):
    config_path = tmp_path / "private-config.json"
    secret = "stage-two-must-not-read-this-secret"
    config_path.write_text(f'{{"api_key": "{secret}"}}', encoding="utf-8")
    sessions = SessionStore("one-time-startup-secret")
    app = create_app(config_path, session_store=sessions)

    with _client(app) as client:
        shell = client.get("/")
        health = client.get("/healthz")

    assert shell.status_code == 200
    assert "Horizon Config" in shell.text
    assert secret not in shell.text
    assert str(config_path) not in shell.text
    assert "one-time-startup-secret" not in shell.text
    assert health.json() == {"status": "ok"}
    assert secret not in health.text
    assert str(config_path) not in health.text


def test_public_responses_apply_restrictive_headers_without_cors(tmp_path: Path):
    app = create_app(tmp_path / "config.json")

    with _client(app) as client:
        response = client.get(
            "/",
            headers={"Origin": "https://attacker.example"},
        )

    assert response.status_code == 200
    assert response.headers["content-security-policy"] == CONTENT_SECURITY_POLICY
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-request-id"]
    assert "access-control-allow-origin" not in response.headers


def test_hostile_host_is_rejected_before_routing(tmp_path: Path):
    app = create_app(tmp_path / "config.json")

    with _client(app) as client:
        response = client.get("/", headers={"Host": "localhost.attacker.example"})

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_host"


@pytest.mark.parametrize("origin", [None, "https://attacker.example"])
def test_bootstrap_requires_loopback_origin_without_consuming_token(
    tmp_path: Path,
    origin: str | None,
):
    token = "valid-one-time-token"
    sessions = SessionStore(token)
    app = create_app(tmp_path / "config.json", session_store=sessions)
    headers = {} if origin is None else {"Origin": origin}

    with _client(app) as client:
        rejected = client.post(
            "/api/v1/session/bootstrap",
            headers=headers,
            json={"token": token},
        )
        accepted = client.post(
            "/api/v1/session/bootstrap",
            headers={"Origin": LOOPBACK_ORIGIN},
            json={"token": token},
        )

    assert rejected.status_code == 403
    assert rejected.json()["error"]["code"] == "invalid_origin"
    assert accepted.status_code == 200


def test_bootstrap_is_single_use_and_sets_strict_http_only_cookie(tmp_path: Path):
    token = "single-use-token"
    sessions = SessionStore(token)
    app = create_app(tmp_path / "config.json", session_store=sessions)

    with _client(app) as client:
        first = client.post(
            "/api/v1/session/bootstrap",
            headers={"Origin": LOOPBACK_ORIGIN},
            json={"token": token},
        )
        second = client.post(
            "/api/v1/session/bootstrap",
            headers={"Origin": LOOPBACK_ORIGIN},
            json={"token": token},
        )
        status = client.get("/api/v1/session")

    assert first.status_code == 200
    cookie = first.headers["set-cookie"]
    assert cookie.startswith(f"{SESSION_COOKIE_NAME}=")
    assert "HttpOnly" in cookie
    assert "SameSite=strict" in cookie
    assert "Path=/" in cookie
    assert second.status_code == 401
    assert second.json()["error"]["code"] == "invalid_bootstrap"
    assert status.status_code == 200
    assert status.json() == first.json()


def test_session_api_rejects_missing_process_local_session(tmp_path: Path):
    app = create_app(tmp_path / "config.json")

    with _client(app) as client:
        response = client.get("/api/v1/session")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_session"


def test_state_changing_api_requires_session_and_matching_csrf(tmp_path: Path):
    token = "csrf-bootstrap-token"
    app = create_app(
        tmp_path / "config.json",
        session_store=SessionStore(token),
    )

    @app.post("/api/v1/test-mutation")
    async def test_mutation() -> dict[str, bool]:
        return {"changed": True}

    with _client(app) as client:
        csrf_token = _bootstrap(client, token)
        missing = client.post(
            "/api/v1/test-mutation",
            headers={"Origin": LOOPBACK_ORIGIN},
        )
        wrong = client.post(
            "/api/v1/test-mutation",
            headers={
                "Origin": LOOPBACK_ORIGIN,
                "X-CSRF-Token": "wrong-token",
            },
        )
        accepted = client.post(
            "/api/v1/test-mutation",
            headers={
                "Origin": LOOPBACK_ORIGIN,
                "X-CSRF-Token": csrf_token,
            },
        )

    assert missing.status_code == 403
    assert missing.json()["error"]["code"] == "invalid_csrf"
    assert wrong.status_code == 403
    assert wrong.json()["error"]["code"] == "invalid_csrf"
    assert accepted.status_code == 200
    assert accepted.json() == {"changed": True}


def test_invalid_bootstrap_body_does_not_echo_input(tmp_path: Path):
    secret = "rejected-secret-value"
    app = create_app(tmp_path / "config.json")

    with _client(app) as client:
        response = client.post(
            "/api/v1/session/bootstrap",
            headers={"Origin": LOOPBACK_ORIGIN},
            json={"unexpected": secret},
        )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"
    assert secret not in response.text


def test_unexpected_exceptions_and_logs_are_sanitized(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
):
    secret = "never-return-or-log-this"
    query_secret = "query-secret-must-not-appear"
    app = create_app(tmp_path / "config.json")

    @app.get("/explode")
    async def explode() -> None:
        raise RuntimeError(secret)

    caplog.set_level(logging.INFO, logger="horizon.config_ui")
    with _client(app) as client:
        response = client.get(f"/explode?token={query_secret}")

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "internal_error"
    assert secret not in response.text
    assert query_secret not in response.text
    assert secret not in caplog.text
    assert query_secret not in caplog.text
    assert "route=/explode" in caplog.text


def test_http_exception_details_are_sanitized(tmp_path: Path):
    secret = "http-exception-detail-must-not-escape"
    app = create_app(tmp_path / "config.json")

    @app.get("/rejected")
    async def rejected() -> None:
        raise HTTPException(status_code=418, detail=secret)

    with _client(app) as client:
        response = client.get("/rejected")

    assert response.status_code == 418
    assert response.json()["error"]["code"] == "request_failed"
    assert secret not in response.text
