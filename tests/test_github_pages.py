from src.models import Config
from src.orchestrator import HorizonOrchestrator
from src.storage.manager import StorageManager


def _config(*, pages_enabled: bool | None = None) -> Config:
    values = {
        "ai": {
            "provider": "openai",
            "model": "test",
            "api_key_env": "OPENAI_API_KEY",
        },
        "sources": {},
        "filtering": {},
    }
    if pages_enabled is not None:
        values["github_pages"] = {"enabled": pages_enabled}
    return Config.model_validate(values)


def test_github_pages_is_disabled_by_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    orchestrator = HorizonOrchestrator(
        _config(),
        StorageManager(data_dir=str(tmp_path / "data")),
    )

    result = orchestrator._publish_github_pages_summary(
        summary="# Daily\n\nBody",
        date="2026-07-21",
        language="en",
    )

    assert result is None
    assert not (tmp_path / "docs").exists()


def test_github_pages_writes_jekyll_post_when_enabled(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    orchestrator = HorizonOrchestrator(
        _config(pages_enabled=True),
        StorageManager(data_dir=str(tmp_path / "data")),
    )

    result = orchestrator._publish_github_pages_summary(
        summary="# Daily\n\nBody",
        date="2026-07-21",
        language="zh",
    )

    expected = tmp_path / "docs/_posts/2026-07-21-summary-zh.md"
    assert result == expected
    content = expected.read_text(encoding="utf-8")
    assert 'title: "Horizon Summary: 2026-07-21 (ZH)"' in content
    assert "# Daily" not in content
    assert content.endswith("Body")
