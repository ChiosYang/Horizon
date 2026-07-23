"""Secret-safe rendering helpers for configuration diagnostics and diffs."""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


REDACTED = "<redacted>"
_SENSITIVE_NAME = re.compile(
    r"(?:^|[_-])(api[_-]?key|authorization|cookie|credential|password|secret|token)(?:$|[_-])",
    re.IGNORECASE,
)
_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_sensitive_name(name: str) -> bool:
    """Return whether a configuration or header name normally carries a secret."""

    normalized = name.lower()
    return not normalized.endswith("_env") and bool(_SENSITIVE_NAME.search(normalized))


def _redact_header_lines(value: str) -> str:
    lines = value.splitlines()
    if not any(":" in line for line in lines):
        return value

    output: list[str] = []
    for line in lines:
        name, separator, header_value = line.partition(":")
        if separator and is_sensitive_name(name.strip()):
            spacing = " " if header_value.startswith(" ") else ""
            line = f"{name}:{spacing}{REDACTED}"
        output.append(line)
    return "\n".join(output)


def _redact_url(value: str) -> str:
    try:
        parts = urlsplit(value)
        if parts.scheme not in {"http", "https"} or not parts.netloc:
            return value

        netloc = parts.netloc
        if parts.username is not None or parts.password is not None:
            netloc = f"{REDACTED}@{parts.hostname or ''}"
            if parts.port is not None:
                netloc += f":{parts.port}"

        query = [
            (name, REDACTED if is_sensitive_name(name) else item_value)
            for name, item_value in parse_qsl(parts.query, keep_blank_values=True)
        ]
        return urlunsplit(
            (parts.scheme, netloc, parts.path, urlencode(query), parts.fragment)
        )
    except (TypeError, ValueError):
        authority = value.split("://", 1)[-1].split("/", 1)[0]
        if "@" in authority:
            return REDACTED
        return value


def redact_config_value(value: Any, key: str = "") -> Any:
    """Return a deep redacted copy suitable for browser-visible output."""

    if key.lower().endswith("_env") and isinstance(value, str):
        return value if _ENV_NAME.fullmatch(value) else REDACTED
    if key and is_sensitive_name(key):
        return REDACTED
    if isinstance(value, dict):
        return {
            item_key: redact_config_value(item_value, str(item_key))
            for item_key, item_value in value.items()
        }
    if isinstance(value, list):
        return [redact_config_value(item) for item in value]
    if not isinstance(value, str):
        return value

    header_safe = _redact_header_lines(value)
    url_safe = _redact_url(header_safe)

    stripped = url_safe.strip()
    if stripped.startswith(("{", "[")):
        try:
            decoded = json.loads(url_safe)
        except json.JSONDecodeError:
            return url_safe
        return json.dumps(redact_config_value(decoded), ensure_ascii=False)
    return url_safe
