import json

import pytest

from src.configuration.backups import BackupError
from src.configuration.document import ConfigDocumentError
from src.configuration.redaction import REDACTED, redact_config_value
from src.configuration.service import (
    ConfigApplicationService,
    ConfigValidationFailed,
    ConfigWarningsNotAcknowledged,
    RevisionConflictError,
)


def _minimal_config():
    return {
        "version": "1.0",
        "ai": {
            "provider": "openai",
            "model": "gpt-4",
            "api_key_env": "TEST_API_KEY",
        },
        "sources": {},
        "filtering": {"ai_score_threshold": 6.0},
    }


def _write_config(path, data):
    path.write_text(
        f"{json.dumps(data, indent=2, ensure_ascii=False)}\n",
        encoding="utf-8",
    )


def test_save_preserves_placeholders_unknown_fields_and_exact_backup(tmp_path):
    path = tmp_path / "data" / "config.json"
    path.parent.mkdir()
    raw = _minimal_config()
    raw["ai"]["base_url"] = "https://${PRIVATE_HOST}/v1"
    raw["future_feature"] = {"mode": "keep-me"}
    _write_config(path, raw)
    original_bytes = path.read_bytes()
    service = ConfigApplicationService(
        path,
        environ={"TEST_API_KEY": "secret", "PRIVATE_HOST": "private.example.com"},
    )
    revision = service.load().revision

    result = service.save(
        [
            {
                "op": "replace",
                "path": "/filtering/ai_score_threshold",
                "value": 7.5,
            }
        ],
        expected_revision=revision,
        acknowledge_warnings=True,
    )

    saved = service.load()
    assert result.changed
    assert result.backup_id is not None
    assert saved.data["ai"]["base_url"] == "https://${PRIVATE_HOST}/v1"
    assert saved.data["future_feature"] == {"mode": "keep-me"}
    backup_path = service.backups.backup_dir / result.backup_id
    assert backup_path.read_bytes() == original_bytes
    assert "private.example.com" not in path.read_text(encoding="utf-8")


def test_save_requires_explicit_warning_acknowledgement(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    original = path.read_bytes()
    service = ConfigApplicationService(path, environ={})
    revision = service.load().revision

    with pytest.raises(ConfigWarningsNotAcknowledged):
        service.save(
            [{"op": "replace", "path": "/filtering/ai_score_threshold", "value": 7}],
            expected_revision=revision,
        )

    assert path.read_bytes() == original
    assert service.list_backups() == []


def test_invalid_candidate_is_not_saved_or_backed_up(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    original = path.read_bytes()
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    with pytest.raises(ConfigValidationFailed):
        service.save(
            [
                {
                    "op": "replace",
                    "path": "/filtering/ai_score_threshold",
                    "value": "not-a-number",
                }
            ],
            expected_revision=service.load().revision,
        )

    assert path.read_bytes() == original
    assert service.list_backups() == []


def test_non_json_candidate_is_rejected_before_backup(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    original = path.read_bytes()
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    with pytest.raises(ConfigDocumentError) as exc_info:
        service.save(
            [
                {
                    "op": "replace",
                    "path": "/filtering/ai_score_threshold",
                    "value": float("nan"),
                }
            ],
            expected_revision=service.load().revision,
        )

    assert exc_info.value.code == "not_json_serializable"
    assert path.read_bytes() == original
    assert service.list_backups() == []


def test_stale_revision_cannot_overwrite_external_change(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})
    stale_revision = service.load().revision
    changed = _minimal_config()
    changed["filtering"]["ai_score_threshold"] = 8.0
    _write_config(path, changed)

    with pytest.raises(RevisionConflictError) as exc_info:
        service.save(
            [{"op": "replace", "path": "/filtering/ai_score_threshold", "value": 9}],
            expected_revision=stale_revision,
        )

    assert exc_info.value.actual == service.load().revision
    assert service.load().data["filtering"]["ai_score_threshold"] == 8.0
    assert service.list_backups() == []


def test_failed_write_is_rolled_back_from_exact_backup(tmp_path, monkeypatch):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    original = path.read_bytes()
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    def corrupt_then_fail(target, content):
        target.write_text("{broken", encoding="utf-8")
        raise OSError("simulated replace failure")

    monkeypatch.setattr("src.configuration.service._atomic_write_text", corrupt_then_fail)

    with pytest.raises(OSError, match="simulated replace failure"):
        service.save(
            [{"op": "replace", "path": "/filtering/ai_score_threshold", "value": 7}],
            expected_revision=service.load().revision,
        )

    assert path.read_bytes() == original
    assert len(service.list_backups()) == 1


def test_create_initial_configuration_without_backup(tmp_path):
    path = tmp_path / "nested" / "config.json"
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    result = service.create(_minimal_config())

    assert result.changed
    assert result.backup_id is None
    assert service.load().revision == result.revision
    assert service.list_backups() == []


def test_create_refuses_to_replace_existing_file(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    with pytest.raises(RevisionConflictError):
        service.create(_minimal_config())


def test_create_race_preserves_external_file(tmp_path, monkeypatch):
    path = tmp_path / "config.json"
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})
    external = _minimal_config()
    external["filtering"]["ai_score_threshold"] = 9

    def external_create_then_conflict(source, destination):
        _write_config(destination, external)
        raise FileExistsError("simulated concurrent create")

    monkeypatch.setattr("src.configuration.service.os.link", external_create_then_conflict)

    with pytest.raises(RevisionConflictError):
        service.create(_minimal_config())

    assert service.load().data["filtering"]["ai_score_threshold"] == 9


def test_restore_creates_rollback_backup_and_restores_selected_version(tmp_path):
    path = tmp_path / "data" / "config.json"
    path.parent.mkdir()
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    first_save = service.save(
        [{"op": "replace", "path": "/filtering/ai_score_threshold", "value": 7}],
        expected_revision=service.load().revision,
    )
    second_save = service.save(
        [{"op": "replace", "path": "/filtering/ai_score_threshold", "value": 8}],
        expected_revision=service.load().revision,
    )

    restored = service.restore(
        first_save.backup_id,
        expected_revision=second_save.revision,
    )

    assert restored.changed
    assert restored.backup_id is not None
    assert service.load().data["filtering"]["ai_score_threshold"] == 6.0
    assert any(info.id == restored.backup_id for info in service.list_backups())


def test_backup_retention_keeps_newest_versions(tmp_path):
    path = tmp_path / "data" / "config.json"
    path.parent.mkdir()
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(
        path,
        backup_retention=2,
        environ={"TEST_API_KEY": "set"},
    )

    for threshold in (7, 8, 9):
        service.save(
            [
                {
                    "op": "replace",
                    "path": "/filtering/ai_score_threshold",
                    "value": threshold,
                }
            ],
            expected_revision=service.load().revision,
        )

    assert len(service.list_backups()) == 2


def test_backup_identifier_cannot_escape_backup_directory(tmp_path):
    path = tmp_path / "data" / "config.json"
    path.parent.mkdir()
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    with pytest.raises(BackupError) as exc_info:
        service.backups.load("../config.json")

    assert exc_info.value.code == "invalid_backup_id"


def test_restore_rejects_backup_changed_after_preview(tmp_path, monkeypatch):
    path = tmp_path / "data" / "config.json"
    path.parent.mkdir()
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})
    saved = service.save(
        [{"op": "replace", "path": "/filtering/ai_score_threshold", "value": 7}],
        expected_revision=service.load().revision,
    )
    active_before = path.read_bytes()
    original_restore = service.backups.restore_bytes

    def tamper_then_restore(backup_id, *, expected_revision=None):
        if backup_id == saved.backup_id:
            tampered = _minimal_config()
            tampered["filtering"]["ai_score_threshold"] = 9
            _write_config(service.backups.backup_dir / backup_id, tampered)
        return original_restore(backup_id, expected_revision=expected_revision)

    monkeypatch.setattr(service.backups, "restore_bytes", tamper_then_restore)

    with pytest.raises(BackupError) as exc_info:
        service.restore(
            saved.backup_id,
            expected_revision=service.load().revision,
        )

    assert exc_info.value.code == "backup_revision_conflict"
    assert path.read_bytes() == active_before


def test_noop_save_does_not_create_backup(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    result = service.save([], expected_revision=service.load().revision)

    assert not result.changed
    assert result.backup_id is None
    assert service.list_backups() == []


def test_diff_redacts_header_and_url_secrets(tmp_path):
    path = tmp_path / "config.json"
    raw = _minimal_config()
    raw["webhook"] = {
        "enabled": False,
        "headers": "Authorization: old-header-secret",
    }
    raw["sources"] = {
        "rss": [
            {
                "name": "Private feed",
                "url": "https://example.com/feed?access_token=old-url-secret",
            }
        ]
    }
    _write_config(path, raw)
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})

    preview = service.preview(
        [
            {
                "op": "replace",
                "path": "/webhook/headers",
                "value": "Authorization: new-header-secret",
            },
            {
                "op": "replace",
                "path": "/sources/rss/0/url",
                "value": "https://example.com/feed?access_token=new-url-secret",
            },
        ],
        expected_revision=service.load().revision,
    )
    serialized = preview.diff.model_dump_json()

    assert "old-header-secret" not in serialized
    assert "new-header-secret" not in serialized
    assert "old-url-secret" not in serialized
    assert "new-url-secret" not in serialized
    assert "redacted" in serialized


def test_redaction_never_returns_malformed_url_userinfo():
    value = "https://private-user:private-password@example.com:bad/feed"

    assert redact_config_value(value) == REDACTED


def test_diff_redacts_secret_misplaced_in_env_name(tmp_path):
    path = tmp_path / "config.json"
    _write_config(path, _minimal_config())
    service = ConfigApplicationService(path, environ={"TEST_API_KEY": "set"})
    misplaced_secret = "sk-private-value-that-is-not-an-env-name"

    preview = service.preview(
        [
            {
                "op": "replace",
                "path": "/ai/api_key_env",
                "value": misplaced_secret,
            }
        ],
        expected_revision=service.load().revision,
    )

    assert misplaced_secret not in preview.diff.model_dump_json()
