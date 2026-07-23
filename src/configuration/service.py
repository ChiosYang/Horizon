"""Application service for safe, lossless Horizon configuration editing."""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
import tempfile
from typing import Any, Mapping, Sequence

from pydantic import BaseModel

from .._file_utils import _atomic_write_text
from .backups import BackupInfo, BackupStore
from .diff import ConfigDiff, build_redacted_diff
from .document import (
    ConfigDocumentError,
    RawConfigDocument,
    compute_revision,
    serialize_raw_config,
)
from .patch import apply_json_patch
from .validation import ValidationReport, ValidationResult, validate_raw_config


class ConfigServiceError(RuntimeError):
    """Base class for safe application-service failures."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class RevisionConflictError(ConfigServiceError):
    """The active file no longer matches the client's revision."""

    def __init__(self, expected: str | None, actual: str | None) -> None:
        super().__init__(
            "revision_conflict",
            "The configuration changed after it was loaded. Reload before saving.",
        )
        self.expected = expected
        self.actual = actual


class ConfigValidationFailed(ConfigServiceError):
    """A candidate has structural validation errors."""

    def __init__(self, report: ValidationReport) -> None:
        super().__init__(
            "configuration_invalid",
            "The configuration contains errors and was not saved.",
        )
        self.report = report


class ConfigWarningsNotAcknowledged(ConfigServiceError):
    """A valid candidate has warnings requiring explicit confirmation."""

    def __init__(self, report: ValidationReport) -> None:
        super().__init__(
            "warnings_not_acknowledged",
            "Review and acknowledge configuration warnings before saving.",
        )
        self.report = report


@dataclass(frozen=True)
class ConfigPreview:
    """A non-persisted candidate and its browser-safe review output."""

    revision: str
    candidate: dict[str, Any] = field(repr=False)
    report: ValidationReport
    diff: ConfigDiff


class SaveResult(BaseModel):
    """Public result of a create, save, or restore operation."""

    changed: bool
    revision: str
    backup_id: str | None = None
    report: ValidationReport
    diff: ConfigDiff


def _atomic_create_text(path: Path, content: str) -> None:
    """Create a complete file atomically without replacing an existing path."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(content.encode("utf-8"))
        os.link(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


class ConfigApplicationService:
    """Coordinate raw editing, validation, revisions, backups, and atomic writes."""

    def __init__(
        self,
        config_path: str | Path = "data/config.json",
        *,
        backup_dir: str | Path | None = None,
        backup_retention: int = 20,
        environ: Mapping[str, str] | None = None,
    ) -> None:
        self.config_path = Path(config_path).resolve()
        self.backups = BackupStore(
            self.config_path,
            backup_dir=backup_dir,
            retention=backup_retention,
        )
        self._environ = environ

    def load(self) -> RawConfigDocument:
        return RawConfigDocument.load(self.config_path)

    def validate(self, data: Mapping[str, Any]) -> ValidationResult:
        return validate_raw_config(data, environ=self._environ)

    def preview(
        self,
        operations: Sequence[Mapping[str, Any]],
        *,
        expected_revision: str,
    ) -> ConfigPreview:
        current = self.load()
        self._require_revision(expected_revision, current.revision)
        candidate = apply_json_patch(current.data, operations)
        candidate = self._require_object(candidate)
        # Reject non-JSON values before validation, diffing, or backup creation.
        serialize_raw_config(candidate)
        result = self.validate(candidate)
        return ConfigPreview(
            revision=current.revision,
            candidate=candidate,
            report=result.report,
            diff=build_redacted_diff(current.data, candidate),
        )

    def create(
        self,
        data: Mapping[str, Any],
        *,
        acknowledge_warnings: bool = False,
    ) -> SaveResult:
        """Create the initial configuration only when no active file exists."""

        if self.config_path.exists():
            raise RevisionConflictError(None, self.load().revision)
        candidate = self._require_object(dict(data))
        validation = self.validate(candidate)
        self._require_saveable(validation.report, acknowledge_warnings)
        config_diff = build_redacted_diff({}, candidate)
        content = serialize_raw_config(candidate)
        expected_revision = compute_revision(content)

        try:
            _atomic_create_text(self.config_path, content)
        except FileExistsError as exc:
            actual = self.load().revision if self.config_path.is_file() else None
            raise RevisionConflictError(None, actual) from exc
        saved = self._reload_validated_or_remove_created(expected_revision)
        return SaveResult(
            changed=True,
            revision=saved.revision,
            report=validation.report,
            diff=config_diff,
        )

    def save(
        self,
        operations: Sequence[Mapping[str, Any]],
        *,
        expected_revision: str,
        acknowledge_warnings: bool = False,
    ) -> SaveResult:
        preview = self.preview(operations, expected_revision=expected_revision)
        self._require_saveable(preview.report, acknowledge_warnings)
        if not preview.diff.changed:
            return SaveResult(
                changed=False,
                revision=preview.revision,
                report=preview.report,
                diff=preview.diff,
            )

        current = self.load()
        self._require_revision(expected_revision, current.revision)
        content = serialize_raw_config(preview.candidate)
        backup = self.backups.create(current)
        try:
            _atomic_write_text(self.config_path, content)
            saved = self._reload_and_require_valid()
        except Exception:
            self.backups.restore_bytes(backup.id)
            raise
        self.backups.prune()
        return SaveResult(
            changed=True,
            revision=saved.revision,
            backup_id=backup.id,
            report=preview.report,
            diff=preview.diff,
        )

    def list_backups(self) -> list[BackupInfo]:
        return self.backups.list()

    def restore(
        self,
        backup_id: str,
        *,
        expected_revision: str,
        acknowledge_warnings: bool = False,
    ) -> SaveResult:
        current = self.load()
        self._require_revision(expected_revision, current.revision)
        target = self.backups.load(backup_id)
        validation = self.validate(target.data)
        self._require_saveable(validation.report, acknowledge_warnings)
        config_diff = build_redacted_diff(current.data, target.data)
        if not config_diff.changed:
            return SaveResult(
                changed=False,
                revision=current.revision,
                report=validation.report,
                diff=config_diff,
            )

        current = self.load()
        self._require_revision(expected_revision, current.revision)
        rollback = self.backups.create(current)
        try:
            self.backups.restore_bytes(
                backup_id,
                expected_revision=target.revision,
            )
            restored = self._reload_and_require_valid()
        except Exception:
            self.backups.restore_bytes(rollback.id)
            raise
        self.backups.prune()
        return SaveResult(
            changed=True,
            revision=restored.revision,
            backup_id=rollback.id,
            report=validation.report,
            diff=config_diff,
        )

    @staticmethod
    def _require_object(value: Any) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise ConfigDocumentError(
                "invalid_root",
                "The configuration root must be a JSON object.",
            )
        return value

    @staticmethod
    def _require_revision(expected: str | None, actual: str | None) -> None:
        if expected != actual:
            raise RevisionConflictError(expected, actual)

    @staticmethod
    def _require_saveable(
        report: ValidationReport,
        acknowledge_warnings: bool,
    ) -> None:
        if not report.valid:
            raise ConfigValidationFailed(report)
        if report.warnings and not acknowledge_warnings:
            raise ConfigWarningsNotAcknowledged(report)

    def _reload_and_require_valid(self) -> RawConfigDocument:
        document = self.load()
        validation = self.validate(document.data)
        if not validation.report.valid:
            raise ConfigValidationFailed(validation.report)
        return document

    def _reload_validated_or_remove_created(
        self,
        expected_revision: str,
    ) -> RawConfigDocument:
        try:
            document = self.load()
            self._require_revision(expected_revision, document.revision)
            validation = self.validate(document.data)
            if not validation.report.valid:
                raise ConfigValidationFailed(validation.report)
            return document
        except Exception:
            try:
                current = self.load()
            except (FileNotFoundError, ConfigDocumentError):
                current = None
            if current is not None and current.revision == expected_revision:
                self.config_path.unlink(missing_ok=True)
            raise
