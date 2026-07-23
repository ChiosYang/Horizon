"""Safe configuration editing primitives for Horizon."""

from .backups import BackupError, BackupInfo, BackupStore
from .diff import ConfigDiff, DiffEntry, build_redacted_diff
from .document import (
    ConfigDocumentError,
    RawConfigDocument,
    compute_revision,
    parse_raw_config,
    serialize_raw_config,
)
from .patch import ConfigPatchError, apply_json_patch, parse_json_pointer
from .service import (
    ConfigApplicationService,
    ConfigPreview,
    ConfigServiceError,
    ConfigValidationFailed,
    ConfigWarningsNotAcknowledged,
    RevisionConflictError,
    SaveResult,
)
from .validation import (
    EffectiveConfig,
    ValidationIssue,
    ValidationReport,
    ValidationResult,
    discover_env_references,
    expand_env_references,
    validate_raw_config,
)

__all__ = [
    "BackupError",
    "BackupInfo",
    "BackupStore",
    "ConfigApplicationService",
    "ConfigDiff",
    "ConfigDocumentError",
    "ConfigPatchError",
    "ConfigPreview",
    "ConfigServiceError",
    "ConfigValidationFailed",
    "ConfigWarningsNotAcknowledged",
    "DiffEntry",
    "EffectiveConfig",
    "RawConfigDocument",
    "RevisionConflictError",
    "SaveResult",
    "ValidationIssue",
    "ValidationReport",
    "ValidationResult",
    "apply_json_patch",
    "build_redacted_diff",
    "compute_revision",
    "discover_env_references",
    "expand_env_references",
    "parse_json_pointer",
    "parse_raw_config",
    "serialize_raw_config",
    "validate_raw_config",
]

