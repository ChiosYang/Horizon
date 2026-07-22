"""A small RFC 6902 JSON Patch implementation for raw configuration edits."""

from __future__ import annotations

from copy import deepcopy
import re
from typing import Any, Mapping, Sequence


_ARRAY_INDEX = re.compile(r"0|[1-9][0-9]*")
_SUPPORTED_OPERATIONS = {"add", "replace", "remove", "move"}


class ConfigPatchError(ValueError):
    """A JSON Patch operation is malformed or cannot be applied."""

    def __init__(self, code: str, path: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message


def parse_json_pointer(pointer: str) -> list[str]:
    """Decode an RFC 6901 JSON Pointer into path tokens."""

    if pointer == "":
        return []
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ConfigPatchError(
            "invalid_pointer",
            pointer if isinstance(pointer, str) else "",
            "A JSON Pointer must be empty or start with '/'.",
        )

    tokens: list[str] = []
    for raw_token in pointer[1:].split("/"):
        if re.search(r"~(?:[^01]|$)", raw_token):
            raise ConfigPatchError(
                "invalid_pointer_escape",
                pointer,
                "A JSON Pointer contains an invalid '~' escape.",
            )
        tokens.append(raw_token.replace("~1", "/").replace("~0", "~"))
    return tokens


def _array_index(token: str, length: int, path: str, *, allow_end: bool) -> int:
    if token == "-" and allow_end:
        return length
    if not _ARRAY_INDEX.fullmatch(token):
        raise ConfigPatchError(
            "invalid_array_index",
            path,
            "The JSON Pointer contains an invalid array index.",
        )
    index = int(token)
    maximum = length if allow_end else length - 1
    if index > maximum:
        raise ConfigPatchError(
            "array_index_out_of_range",
            path,
            "The JSON Pointer array index is out of range.",
        )
    return index


def _resolve_parent(document: Any, tokens: Sequence[str], path: str) -> tuple[Any, str]:
    if not tokens:
        raise ConfigPatchError(
            "root_has_no_parent",
            path,
            "The document root does not have a parent container.",
        )

    current = document
    for token in tokens[:-1]:
        if isinstance(current, dict):
            if token not in current:
                raise ConfigPatchError(
                    "path_not_found",
                    path,
                    "The JSON Pointer does not identify an existing parent.",
                )
            current = current[token]
        elif isinstance(current, list):
            current = current[_array_index(token, len(current), path, allow_end=False)]
        else:
            raise ConfigPatchError(
                "invalid_parent",
                path,
                "The JSON Pointer traverses a value that is not a container.",
            )
    return current, tokens[-1]


def _get(document: Any, tokens: Sequence[str], path: str) -> Any:
    current = document
    for token in tokens:
        if isinstance(current, dict):
            if token not in current:
                raise ConfigPatchError(
                    "path_not_found",
                    path,
                    "The JSON Pointer does not identify an existing value.",
                )
            current = current[token]
        elif isinstance(current, list):
            current = current[_array_index(token, len(current), path, allow_end=False)]
        else:
            raise ConfigPatchError(
                "invalid_parent",
                path,
                "The JSON Pointer traverses a value that is not a container.",
            )
    return current


def _add(document: Any, tokens: Sequence[str], value: Any, path: str) -> Any:
    if not tokens:
        return deepcopy(value)
    parent, token = _resolve_parent(document, tokens, path)
    if isinstance(parent, dict):
        parent[token] = deepcopy(value)
        return document
    if isinstance(parent, list):
        index = _array_index(token, len(parent), path, allow_end=True)
        parent.insert(index, deepcopy(value))
        return document
    raise ConfigPatchError(
        "invalid_parent",
        path,
        "The JSON Pointer parent is not an object or array.",
    )


def _remove(document: Any, tokens: Sequence[str], path: str) -> tuple[Any, Any]:
    if not tokens:
        return None, document
    parent, token = _resolve_parent(document, tokens, path)
    if isinstance(parent, dict):
        if token not in parent:
            raise ConfigPatchError(
                "path_not_found",
                path,
                "The JSON Pointer does not identify an existing value.",
            )
        return document, parent.pop(token)
    if isinstance(parent, list):
        index = _array_index(token, len(parent), path, allow_end=False)
        return document, parent.pop(index)
    raise ConfigPatchError(
        "invalid_parent",
        path,
        "The JSON Pointer parent is not an object or array.",
    )


def _replace(document: Any, tokens: Sequence[str], value: Any, path: str) -> Any:
    if not tokens:
        return deepcopy(value)
    parent, token = _resolve_parent(document, tokens, path)
    if isinstance(parent, dict):
        if token not in parent:
            raise ConfigPatchError(
                "path_not_found",
                path,
                "The JSON Pointer does not identify an existing value.",
            )
        parent[token] = deepcopy(value)
        return document
    if isinstance(parent, list):
        parent[_array_index(token, len(parent), path, allow_end=False)] = deepcopy(value)
        return document
    raise ConfigPatchError(
        "invalid_parent",
        path,
        "The JSON Pointer parent is not an object or array.",
    )


def apply_json_patch(
    document: Any,
    operations: Sequence[Mapping[str, Any]],
) -> Any:
    """Apply supported RFC 6902 operations to a deep copy of ``document``."""

    result = deepcopy(document)
    for operation in operations:
        if not isinstance(operation, Mapping):
            raise ConfigPatchError(
                "invalid_operation",
                "",
                "Every JSON Patch operation must be an object.",
            )

        op = operation.get("op")
        path = operation.get("path")
        if op not in _SUPPORTED_OPERATIONS:
            raise ConfigPatchError(
                "unsupported_operation",
                path if isinstance(path, str) else "",
                "The JSON Patch operation is not supported.",
            )
        if not isinstance(path, str):
            raise ConfigPatchError(
                "invalid_pointer",
                "",
                "Every JSON Patch operation requires a string path.",
            )

        tokens = parse_json_pointer(path)
        if op in {"add", "replace"}:
            if "value" not in operation:
                raise ConfigPatchError(
                    "missing_value",
                    path,
                    f"The '{op}' operation requires a value.",
                )
            if op == "add":
                result = _add(result, tokens, operation["value"], path)
            else:
                _get(result, tokens, path)
                result = _replace(result, tokens, operation["value"], path)
            continue

        if op == "remove":
            result, _ = _remove(result, tokens, path)
            continue

        from_path = operation.get("from")
        if not isinstance(from_path, str):
            raise ConfigPatchError(
                "missing_from",
                path,
                "The 'move' operation requires a string 'from' pointer.",
            )
        from_tokens = parse_json_pointer(from_path)
        if len(tokens) > len(from_tokens) and tokens[: len(from_tokens)] == from_tokens:
            raise ConfigPatchError(
                "move_into_child",
                path,
                "A value cannot be moved into one of its own descendants.",
            )
        _get(result, from_tokens, from_path)
        result, moved = _remove(result, from_tokens, from_path)
        result = _add(result, tokens, moved, path)

    return result
