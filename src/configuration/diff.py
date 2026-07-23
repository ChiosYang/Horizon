"""Structured, redacted diffs for raw Horizon configuration documents."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from .redaction import redact_config_value


class DiffEntry(BaseModel):
    """One browser-safe raw configuration change."""

    op: Literal["add", "remove", "replace"]
    path: str
    before: Any = None
    after: Any = None


class ConfigDiff(BaseModel):
    """A set of browser-safe changes between two raw documents."""

    entries: list[DiffEntry] = Field(default_factory=list)

    @property
    def changed(self) -> bool:
        return bool(self.entries)


def _pointer(path: str, token: str | int) -> str:
    encoded = str(token).replace("~", "~0").replace("/", "~1")
    return f"{path}/{encoded}" if path else f"/{encoded}"


def _leaf_key(path: str) -> str:
    if not path:
        return ""
    token = path.rsplit("/", 1)[-1]
    return token.replace("~1", "/").replace("~0", "~")


def build_redacted_diff(before: Any, after: Any) -> ConfigDiff:
    """Recursively compare JSON values and redact every emitted value."""

    entries: list[DiffEntry] = []

    def walk(old: Any, new: Any, path: str) -> None:
        if type(old) is not type(new):
            key = _leaf_key(path)
            entries.append(
                DiffEntry(
                    op="replace",
                    path=path,
                    before=redact_config_value(old, key),
                    after=redact_config_value(new, key),
                )
            )
            return

        if isinstance(old, dict):
            old_keys = set(old)
            new_keys = set(new)
            for key in sorted(old_keys - new_keys, key=str):
                item_path = _pointer(path, key)
                entries.append(
                    DiffEntry(
                        op="remove",
                        path=item_path,
                        before=redact_config_value(old[key], str(key)),
                    )
                )
            for key in sorted(new_keys - old_keys, key=str):
                item_path = _pointer(path, key)
                entries.append(
                    DiffEntry(
                        op="add",
                        path=item_path,
                        after=redact_config_value(new[key], str(key)),
                    )
                )
            for key in sorted(old_keys & new_keys, key=str):
                walk(old[key], new[key], _pointer(path, key))
            return

        if isinstance(old, list):
            shared = min(len(old), len(new))
            for index in range(shared):
                walk(old[index], new[index], _pointer(path, index))
            for index in range(len(old) - 1, shared - 1, -1):
                entries.append(
                    DiffEntry(
                        op="remove",
                        path=_pointer(path, index),
                        before=redact_config_value(old[index]),
                    )
                )
            for index in range(shared, len(new)):
                entries.append(
                    DiffEntry(
                        op="add",
                        path=_pointer(path, index),
                        after=redact_config_value(new[index]),
                    )
                )
            return

        if old != new:
            key = _leaf_key(path)
            entries.append(
                DiffEntry(
                    op="replace",
                    path=path,
                    before=redact_config_value(old, key),
                    after=redact_config_value(new, key),
                )
            )

    walk(before, after, "")
    return ConfigDiff(entries=entries)
