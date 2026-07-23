"""Timestamped, contained backups for raw Horizon configuration files."""

from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import re
import tempfile

from pydantic import BaseModel

from .document import RawConfigDocument, compute_revision


_BACKUP_ID = re.compile(
    r"^config-(?P<timestamp>[0-9]{8}T[0-9]{12}Z)-(?P<revision>[0-9a-f]{8})\.json$"
)


class BackupError(ValueError):
    """A backup identifier or operation is invalid."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class BackupInfo(BaseModel):
    """Public metadata for one server-generated backup."""

    id: str
    created_at: datetime
    revision: str
    size: int


def _atomic_write_bytes(path: Path, content: bytes) -> None:
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
            temp_file.write(content)
        os.replace(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


class BackupStore:
    """Manage bounded backup history without exposing filesystem paths."""

    def __init__(
        self,
        config_path: str | Path,
        backup_dir: str | Path | None = None,
        retention: int = 20,
    ) -> None:
        if retention < 1:
            raise ValueError("Backup retention must be at least one.")
        self.config_path = Path(config_path).resolve()
        self.backup_dir = (
            Path(backup_dir).resolve()
            if backup_dir is not None
            else (self.config_path.parent / "config-backups").resolve()
        )
        self.retention = retention

    def create(self, document: RawConfigDocument) -> BackupInfo:
        """Copy the exact current bytes to a new timestamped backup."""

        if document.path != self.config_path:
            raise BackupError(
                "unexpected_config_path",
                "The document does not belong to this backup store.",
            )
        content = document.path.read_bytes()
        if compute_revision(content) != document.revision:
            raise BackupError(
                "stale_document",
                "The active configuration changed before it could be backed up.",
            )

        now = datetime.now(timezone.utc)
        short_revision = document.revision.removeprefix("sha256:")[:8]
        backup_id = f"config-{now.strftime('%Y%m%dT%H%M%S%fZ')}-{short_revision}.json"
        backup_path = self._resolve_id(backup_id, require_exists=False)
        _atomic_write_bytes(backup_path, content)
        return self._info(backup_path)

    def list(self) -> list[BackupInfo]:
        """List valid backups newest first."""

        if not self.backup_dir.exists():
            return []
        backups = [
            self._info(path)
            for path in self.backup_dir.iterdir()
            if path.is_file() and _BACKUP_ID.fullmatch(path.name)
        ]
        backups.sort(key=lambda item: (item.created_at, item.id), reverse=True)
        return backups

    def load(self, backup_id: str) -> RawConfigDocument:
        return RawConfigDocument.load(self._resolve_id(backup_id, require_exists=True))

    def restore_bytes(
        self,
        backup_id: str,
        *,
        expected_revision: str | None = None,
    ) -> None:
        """Atomically replace the active file with exact backup bytes."""

        backup_path = self._resolve_id(backup_id, require_exists=True)
        content = backup_path.read_bytes()
        actual_revision = compute_revision(content)
        if expected_revision is not None and actual_revision != expected_revision:
            raise BackupError(
                "backup_revision_conflict",
                "The backup changed after it was loaded.",
            )
        _atomic_write_bytes(self.config_path, content)

    def prune(self) -> list[str]:
        """Remove backups older than the frozen retention limit."""

        backups = self.list()
        if len(backups) <= self.retention:
            return []
        removed: list[str] = []
        for info in backups[self.retention :]:
            path = self._resolve_id(info.id, require_exists=True)
            path.unlink()
            removed.append(info.id)
        return removed

    def _resolve_id(self, backup_id: str, *, require_exists: bool) -> Path:
        if not isinstance(backup_id, str) or not _BACKUP_ID.fullmatch(backup_id):
            raise BackupError("invalid_backup_id", "The backup identifier is invalid.")
        candidate = (self.backup_dir / backup_id).resolve()
        if candidate.parent != self.backup_dir:
            raise BackupError(
                "backup_path_escape",
                "The backup identifier resolves outside the backup directory.",
            )
        if require_exists and not candidate.is_file():
            raise BackupError("backup_not_found", "The requested backup does not exist.")
        return candidate

    def _info(self, path: Path) -> BackupInfo:
        match = _BACKUP_ID.fullmatch(path.name)
        if match is None:
            raise BackupError("invalid_backup_id", "The backup identifier is invalid.")
        created_at = datetime.strptime(
            match.group("timestamp"), "%Y%m%dT%H%M%S%fZ"
        ).replace(tzinfo=timezone.utc)
        content = path.read_bytes()
        return BackupInfo(
            id=path.name,
            created_at=created_at,
            revision=compute_revision(content),
            size=len(content),
        )
