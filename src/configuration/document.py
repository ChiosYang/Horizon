"""Raw Horizon configuration documents.

The editor persists this unexpanded representation. Runtime expansion belongs
to :mod:`src.configuration.validation` and must never feed the save path.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


REVISION_PREFIX = "sha256:"


class ConfigDocumentError(ValueError):
    """A raw configuration document could not be decoded or parsed."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def compute_revision(content: bytes | str) -> str:
    """Return the stable content revision used for optimistic concurrency."""

    encoded = content.encode("utf-8") if isinstance(content, str) else content
    return f"{REVISION_PREFIX}{hashlib.sha256(encoded).hexdigest()}"


def parse_raw_config(source_text: str) -> dict[str, Any]:
    """Parse one unexpanded JSON object without exposing rejected input."""

    try:
        value = json.loads(source_text)
    except json.JSONDecodeError as exc:
        raise ConfigDocumentError(
            "invalid_json",
            f"Invalid JSON at line {exc.lineno}, column {exc.colno}.",
        ) from exc

    if not isinstance(value, dict):
        raise ConfigDocumentError(
            "invalid_root",
            "The configuration root must be a JSON object.",
        )
    return value


def serialize_raw_config(data: Mapping[str, Any]) -> str:
    """Serialize raw configuration deterministically without expanding it."""

    try:
        return f"{json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False)}\n"
    except (TypeError, ValueError) as exc:
        raise ConfigDocumentError(
            "not_json_serializable",
            "The configuration contains a value that cannot be represented as JSON.",
        ) from exc


@dataclass(frozen=True)
class RawConfigDocument:
    """An unexpanded configuration file and its concurrency revision."""

    path: Path
    source_text: str
    data: dict[str, Any]
    revision: str

    @classmethod
    def load(cls, path: str | Path) -> "RawConfigDocument":
        resolved = Path(path).resolve()
        source_bytes = resolved.read_bytes()
        try:
            encoding = "utf-8-sig" if source_bytes.startswith(b"\xef\xbb\xbf") else "utf-8"
            source_text = source_bytes.decode(encoding)
        except UnicodeDecodeError as exc:
            raise ConfigDocumentError(
                "invalid_encoding",
                "The configuration file must be valid UTF-8.",
            ) from exc

        return cls(
            path=resolved,
            source_text=source_text,
            data=parse_raw_config(source_text),
            revision=compute_revision(source_bytes),
        )

    @classmethod
    def from_text(cls, path: str | Path, source_text: str) -> "RawConfigDocument":
        """Build a document from trusted in-memory UTF-8 text."""

        return cls(
            path=Path(path).resolve(),
            source_text=source_text,
            data=parse_raw_config(source_text),
            revision=compute_revision(source_text),
        )

