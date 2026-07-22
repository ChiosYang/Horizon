"""Environment resolution and secret-safe validation for raw configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
import os
import re
from types import UnionType
from typing import Annotated, Any, Literal, Mapping, Union, get_args, get_origin

from pydantic import BaseModel, Field, ValidationError

from ..models import AIProvider, Config


ENV_VAR_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
ENV_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ValidationIssue(BaseModel):
    """One browser-safe issue at a JSON Pointer path."""

    severity: Literal["error", "warning", "info"]
    path: str
    code: str
    message: str


class ValidationReport(BaseModel):
    """Public validation output that never contains effective values."""

    valid: bool
    issues: list[ValidationIssue] = Field(default_factory=list)
    referenced_env: list[str] = Field(default_factory=list)
    missing_env: list[str] = Field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]


@dataclass(frozen=True)
class EffectiveConfig:
    """Validated runtime configuration whose model may contain expanded values."""

    model: Config = field(repr=False)
    referenced_env: frozenset[str]
    missing_env: frozenset[str]


@dataclass(frozen=True)
class ValidationResult:
    """Internal validation result pairing a safe report with an effective model."""

    report: ValidationReport
    effective_config: EffectiveConfig | None = field(default=None, repr=False)


def discover_env_references(value: Any) -> set[str]:
    """Find every ``${VAR}`` reference in a raw JSON value."""

    found: set[str] = set()
    if isinstance(value, str):
        found.update(ENV_VAR_PATTERN.findall(value))
    elif isinstance(value, dict):
        for item in value.values():
            found.update(discover_env_references(item))
    elif isinstance(value, list):
        for item in value:
            found.update(discover_env_references(item))
    return found


def expand_env_references(value: Any, environ: Mapping[str, str]) -> Any:
    """Return a recursively expanded copy, leaving unknown references intact."""

    if isinstance(value, str):
        return ENV_VAR_PATTERN.sub(
            lambda match: environ.get(match.group(1), match.group(0)),
            value,
        )
    if isinstance(value, dict):
        return {
            key: expand_env_references(item, environ)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [expand_env_references(item, environ) for item in value]
    return value


def _pointer(path: str, token: str | int) -> str:
    encoded = str(token).replace("~", "~0").replace("/", "~1")
    return f"{path}/{encoded}" if path else f"/{encoded}"


def _placeholder_paths(value: Any, path: str = "") -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    if isinstance(value, str):
        for name in ENV_VAR_PATTERN.findall(value):
            found.setdefault(name, set()).add(path)
    elif isinstance(value, dict):
        for key, item in value.items():
            for name, paths in _placeholder_paths(item, _pointer(path, key)).items():
                found.setdefault(name, set()).update(paths)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            for name, paths in _placeholder_paths(item, _pointer(path, index)).items():
                found.setdefault(name, set()).update(paths)
    return found


def _raw_env_name_paths(value: Any, path: str = "") -> dict[str, set[str]]:
    """Best-effort credential references used when model validation fails."""

    found: dict[str, set[str]] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = _pointer(path, key)
            if key.lower().endswith("_env") and isinstance(item, str) and item:
                if ENV_NAME_PATTERN.fullmatch(item):
                    found.setdefault(item, set()).add(item_path)
            for name, paths in _raw_env_name_paths(item, item_path).items():
                found.setdefault(name, set()).update(paths)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            for name, paths in _raw_env_name_paths(item, _pointer(path, index)).items():
                found.setdefault(name, set()).update(paths)
    return found


def _credential_env_paths(
    config: Config,
) -> tuple[dict[str, set[str]], list[str]]:
    found: dict[str, set[str]] = {}
    invalid_paths: list[str] = []

    def add(name: str | None, path: str) -> None:
        if name:
            if ENV_NAME_PATTERN.fullmatch(name):
                found.setdefault(name, set()).add(path)
            else:
                invalid_paths.append(path)

    add(config.ai.api_key_env, "/ai/api_key_env")
    if config.ai.provider == AIProvider.AZURE:
        add(config.ai.azure_endpoint_env, "/ai/azure_endpoint_env")

    for stage in config.ai.stages:
        effective = config.ai.for_stage(stage)
        stage_name = stage.value if hasattr(stage, "value") else str(stage)
        add(effective.api_key_env, f"/ai/stages/{stage_name}/api_key_env")
        if effective.provider == AIProvider.AZURE:
            add(
                effective.azure_endpoint_env,
                f"/ai/stages/{stage_name}/azure_endpoint_env",
            )

    email = getattr(config, "email", None)
    if email is not None and email.enabled:
        add(email.password_env, "/email/password_env")

    webhook = getattr(config, "webhook", None)
    if webhook is not None and webhook.enabled:
        add(webhook.url_env, "/webhook/url_env")

    twitter = getattr(config.sources, "twitter", None)
    if twitter is not None and twitter.enabled and twitter.mode == "apify":
        add(twitter.apify_token_env, "/sources/twitter/apify_token_env")

    return found, invalid_paths


def _unwrap_annotation(annotation: Any) -> Any:
    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation


def _model_candidates(annotation: Any) -> list[type[BaseModel]]:
    annotation = _unwrap_annotation(annotation)
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return [annotation]
    if get_origin(annotation) in {Union, UnionType}:
        candidates: list[type[BaseModel]] = []
        for item in get_args(annotation):
            candidates.extend(_model_candidates(item))
        return candidates
    return []


def _choose_model(annotation: Any, value: Any) -> type[BaseModel] | None:
    candidates = _model_candidates(annotation)
    if not candidates:
        return None
    if len(candidates) == 1 or not isinstance(value, dict):
        return candidates[0]

    discriminator = value.get("type")
    if discriminator is not None:
        for candidate in candidates:
            field_info = candidate.model_fields.get("type")
            if field_info is None:
                continue
            default = field_info.default
            if getattr(default, "value", default) == discriminator:
                return candidate

    return max(
        candidates,
        key=lambda candidate: len(set(candidate.model_fields).intersection(value)),
    )


def _unknown_field_issues(
    value: Any,
    annotation: Any = Config,
    path: str = "",
) -> list[ValidationIssue]:
    annotation = _unwrap_annotation(annotation)
    model = _choose_model(annotation, value)
    issues: list[ValidationIssue] = []

    if model is not None and isinstance(value, dict):
        fields = model.model_fields
        for key, item in value.items():
            item_path = _pointer(path, key)
            field_info = fields.get(key)
            if field_info is None:
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        path=item_path,
                        code="unknown_config_field",
                        message=f"Unknown configuration field '{key}' will be preserved.",
                    )
                )
                continue
            issues.extend(
                _unknown_field_issues(item, field_info.annotation, item_path)
            )
        return issues

    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in {list, tuple, set, frozenset} and isinstance(value, list) and args:
        for index, item in enumerate(value):
            issues.extend(_unknown_field_issues(item, args[0], _pointer(path, index)))
        return issues
    if origin is dict and isinstance(value, dict) and len(args) == 2:
        for key, item in value.items():
            issues.extend(_unknown_field_issues(item, args[1], _pointer(path, key)))
        return issues
    if origin in {Union, UnionType}:
        selected = _choose_model(annotation, value)
        if selected is not None:
            return _unknown_field_issues(value, selected, path)
    return issues


def _location_pointer(location: tuple[Any, ...]) -> str:
    path = ""
    for item in location:
        path = _pointer(path, item)
    return path


def _safe_error_message(error_type: str) -> str:
    if error_type == "missing":
        return "A required configuration value is missing."
    if "url" in error_type:
        return "Enter a valid HTTP or HTTPS URL."
    if error_type in {"enum", "literal_error"}:
        return "Choose a supported configuration value."
    if error_type.startswith(("int_", "float_", "bool_", "string_", "list_", "dict_")):
        return "Enter a value of the expected type."
    if error_type in {
        "greater_than",
        "greater_than_equal",
        "less_than",
        "less_than_equal",
        "too_short",
        "too_long",
    }:
        return "The value is outside the allowed range."
    return "The value does not satisfy the configuration constraint."


def _pydantic_issues(
    error: ValidationError,
    environ: Mapping[str, str],
) -> tuple[list[ValidationIssue], set[str]]:
    issues: list[ValidationIssue] = []
    missing_error_names: set[str] = set()
    for item in error.errors(include_url=False):
        path = _location_pointer(tuple(item.get("loc", ())))
        input_value = item.get("input")
        unresolved = {
            name
            for name in discover_env_references(input_value)
            if not environ.get(name)
        }
        if unresolved:
            missing_error_names.update(unresolved)
            names = ", ".join(sorted(unresolved))
            issues.append(
                ValidationIssue(
                    severity="error",
                    path=path,
                    code="missing_env",
                    message=f"Set environment variable(s) {names} to validate this field.",
                )
            )
            continue

        error_type = str(item.get("type", "value_error"))
        issues.append(
            ValidationIssue(
                severity="error",
                path=path,
                code=error_type.replace(".", "_"),
                message=_safe_error_message(error_type),
            )
        )
    return issues, missing_error_names


def validate_raw_config(
    data: Mapping[str, Any],
    environ: Mapping[str, str] | None = None,
) -> ValidationResult:
    """Validate raw JSON while keeping all expanded values out of the report."""

    active_environ = os.environ if environ is None else environ
    raw_data = dict(data)
    placeholder_paths = _placeholder_paths(raw_data)
    referenced = set(placeholder_paths)
    missing = {name for name in referenced if not active_environ.get(name)}
    issues = _unknown_field_issues(raw_data)
    effective: EffectiveConfig | None = None
    missing_error_names: set[str] = set()

    expanded = expand_env_references(raw_data, active_environ)
    try:
        model = Config.model_validate(expanded)
    except ValidationError as exc:
        validation_issues, missing_error_names = _pydantic_issues(exc, active_environ)
        issues.extend(validation_issues)
        credential_paths = _raw_env_name_paths(raw_data)
    else:
        credential_paths, invalid_env_paths = _credential_env_paths(model)
        issues.extend(
            ValidationIssue(
                severity="warning",
                path=path,
                code="invalid_env_name",
                message="Use an environment-variable name here, not a secret value.",
            )
            for path in invalid_env_paths
        )
        referenced.update(credential_paths)
        missing.update(
            name for name in credential_paths if not active_environ.get(name)
        )
        effective = EffectiveConfig(
            model=model,
            referenced_env=frozenset(referenced),
            missing_env=frozenset(missing),
        )

    referenced.update(credential_paths)
    missing.update(name for name in credential_paths if not active_environ.get(name))

    existing_missing_issue_names = set(missing_error_names)
    for name in sorted(missing):
        if name in existing_missing_issue_names:
            continue
        paths = placeholder_paths.get(name) or credential_paths.get(name) or {""}
        issues.append(
            ValidationIssue(
                severity="warning",
                path=sorted(paths)[0],
                code="missing_env",
                message=f"Environment variable {name} is not set.",
            )
        )

    issues.sort(key=lambda issue: (issue.path, issue.severity, issue.code))
    report = ValidationReport(
        valid=not any(issue.severity == "error" for issue in issues),
        issues=issues,
        referenced_env=sorted(referenced),
        missing_env=sorted(missing),
    )
    return ValidationResult(report=report, effective_config=effective)
