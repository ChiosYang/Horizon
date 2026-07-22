import asyncio
import json
from datetime import datetime, timezone

import pytest

from src.ai.tokens import get_usage_snapshot, record_usage
from src.models import (
    AIConfig,
    Config,
    ContentItem,
    FilteringConfig,
    SourceType,
    SourcesConfig,
)
from src.orchestrator import HorizonOrchestrator
from src.performance import PerformanceRecorder
from src.storage.manager import StorageManager


def _config() -> Config:
    return Config(
        ai=AIConfig(
            provider="openai",
            model="test",
            api_key_env="TEST_API_KEY",
            languages=[],
        ),
        sources=SourcesConfig(),
        filtering=FilteringConfig(ai_score_threshold=7.0),
    )


def _item() -> ContentItem:
    return ContentItem(
        id="rss:test",
        source_type=SourceType.RSS,
        title="Test item",
        url="https://example.com/test",
        published_at=datetime.now(timezone.utc),
    )


def test_token_snapshots_are_immutable_copies() -> None:
    provider = "performance-snapshot-test"
    before = get_usage_snapshot()
    before_provider_total = (
        before.per_provider[provider].total
        if provider in before.per_provider
        else None
    )

    record_usage(provider, input_tokens=7, output_tokens=3)

    if before_provider_total is None:
        assert provider not in before.per_provider
    else:
        assert before.per_provider[provider].total == before_provider_total


def test_recorder_tracks_counts_attributes_and_stage_token_delta() -> None:
    recorder = PerformanceRecorder(run_id="test-run")

    with recorder.stage(
        "analyze_content",
        input_items=2,
        attributes={"model": "test"},
    ) as measurement:
        record_usage("performance-stage-test", input_tokens=11, output_tokens=5)
        measurement.set_result(output_items=2)

    recorder.finish("success")
    report = recorder.to_dict()

    assert report["schema_version"] == 1
    assert report["status"] == "success"
    assert report["tokens"]["total_tokens"] == 16
    stage = report["stages"][0]
    assert stage["name"] == "analyze_content"
    assert stage["status"] == "success"
    assert stage["input_items"] == 2
    assert stage["output_items"] == 2
    assert stage["attributes"] == {"model": "test"}
    assert stage["tokens"]["total_tokens"] == 16
    assert stage["duration_ms"] >= 0


def test_recorder_marks_unhandled_stage_exception() -> None:
    recorder = PerformanceRecorder(run_id="failed-run")

    with pytest.raises(ValueError, match="broken"):
        with recorder.stage("fetch_sources"):
            raise ValueError("broken")

    recorder.finish("failure", error_type="ValueError")
    report = recorder.to_dict()

    assert report["status"] == "failure"
    assert report["error_type"] == "ValueError"
    assert report["stages"][0]["status"] == "failure"
    assert report["stages"][0]["error_type"] == "ValueError"


def test_storage_saves_performance_report_atomically(tmp_path) -> None:
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    report = {"schema_version": 1, "run_id": "safe-run", "status": "success"}

    path = storage.save_performance_report("safe-run", report)

    assert path.parent == storage.metrics_dir.resolve()
    assert json.loads(path.read_text(encoding="utf-8")) == report


def test_storage_rejects_performance_report_path_escape(tmp_path) -> None:
    storage = StorageManager(data_dir=str(tmp_path / "data"))

    with pytest.raises(ValueError, match="Invalid performance run id"):
        storage.save_performance_report("../../outside", {"status": "failure"})


def test_source_fetch_measurement_records_status_and_count() -> None:
    class Scraper:
        async def fetch(self, since):  # type: ignore[no-untyped-def]
            return [_item()]

    orchestrator = HorizonOrchestrator(_config(), storage=object())  # type: ignore[arg-type]
    recorder = PerformanceRecorder(run_id="source-run")
    orchestrator._performance_recorder = recorder

    outcome = asyncio.run(
        orchestrator._fetch_with_progress(
            "RSS Feeds",
            Scraper(),
            datetime.now(timezone.utc),
        )
    )
    recorder.finish("success")
    source_metric = recorder.to_dict()["source_fetches"][0]

    assert outcome.status == "success"
    assert source_metric["name"] == "fetch_source"
    assert source_metric["status"] == "success"
    assert source_metric["output_items"] == 1
    assert source_metric["attributes"] == {"source": "RSS Feeds"}


def test_source_fetch_measurement_records_handled_failure() -> None:
    class Scraper:
        async def fetch(self, since):  # type: ignore[no-untyped-def]
            raise TimeoutError("source timed out")

    orchestrator = HorizonOrchestrator(_config(), storage=object())  # type: ignore[arg-type]
    recorder = PerformanceRecorder(run_id="failed-source-run")
    orchestrator._performance_recorder = recorder

    outcome = asyncio.run(
        orchestrator._fetch_with_progress(
            "RSS Feeds",
            Scraper(),
            datetime.now(timezone.utc),
        )
    )
    recorder.finish("failure", error_type="TimeoutError")
    source_metric = recorder.to_dict()["source_fetches"][0]

    assert outcome.status == "failure"
    assert source_metric["status"] == "failure"
    assert source_metric["error_type"] == "TimeoutError"
    assert source_metric["output_items"] == 0


def test_native_run_persists_stage_metrics_and_token_deltas(
    tmp_path,
    monkeypatch,
) -> None:
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    orchestrator = HorizonOrchestrator(_config(), storage)
    items = [_item()]

    async def fetch_all_sources(since):  # type: ignore[no-untyped-def]
        return items

    async def analyze_content(input_items):  # type: ignore[no-untyped-def]
        record_usage("performance-integration-analysis", 13, 4)
        for item in input_items:
            item.ai_score = 9.0
        return input_items

    async def merge_topic_duplicates(input_items, *, log=True):  # type: ignore[no-untyped-def]
        return input_items

    async def expand_twitter_discussion(input_items):  # type: ignore[no-untyped-def]
        return None

    async def enrich_important_items(input_items):  # type: ignore[no-untyped-def]
        record_usage("performance-integration-enrichment", 8, 2)

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)
    monkeypatch.setattr(orchestrator, "_analyze_content", analyze_content)
    monkeypatch.setattr(
        orchestrator,
        "merge_topic_duplicates",
        merge_topic_duplicates,
    )
    monkeypatch.setattr(
        orchestrator,
        "_expand_twitter_discussion",
        expand_twitter_discussion,
    )
    monkeypatch.setattr(
        orchestrator,
        "_enrich_important_items",
        enrich_important_items,
    )

    asyncio.run(orchestrator.run())

    metric_files = list(storage.metrics_dir.glob("horizon-performance-*.json"))
    assert len(metric_files) == 1
    report = json.loads(metric_files[0].read_text(encoding="utf-8"))
    stages = {stage["name"]: stage for stage in report["stages"]}
    assert report["status"] == "success"
    assert report["tokens"]["total_tokens"] == 27
    assert stages["fetch_sources"]["output_items"] == 1
    assert stages["merge_cross_source_duplicates"]["input_items"] == 1
    assert stages["analyze_content"]["tokens"]["total_tokens"] == 17
    assert stages["filter_and_topic_deduplicate"]["output_items"] == 1
    assert stages["enrich_content"]["tokens"]["total_tokens"] == 10
    assert orchestrator.last_performance_report == report


def test_native_run_persists_no_content_metrics(tmp_path, monkeypatch) -> None:
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    orchestrator = HorizonOrchestrator(_config(), storage)

    async def fetch_all_sources(since):  # type: ignore[no-untyped-def]
        return []

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)

    asyncio.run(orchestrator.run())

    metric_files = list(storage.metrics_dir.glob("horizon-performance-*.json"))
    assert len(metric_files) == 1
    report = json.loads(metric_files[0].read_text(encoding="utf-8"))
    assert report["status"] == "no_content"
    assert report["stages"][-1]["name"] == "fetch_sources"
    assert report["stages"][-1]["output_items"] == 0


def test_native_run_persists_failure_metrics(tmp_path, monkeypatch) -> None:
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    orchestrator = HorizonOrchestrator(_config(), storage)

    async def fetch_all_sources(since):  # type: ignore[no-untyped-def]
        raise RuntimeError("fetch failed")

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)

    with pytest.raises(RuntimeError, match="fetch failed"):
        asyncio.run(orchestrator.run())

    metric_files = list(storage.metrics_dir.glob("horizon-performance-*.json"))
    assert len(metric_files) == 1
    report = json.loads(metric_files[0].read_text(encoding="utf-8"))
    assert report["status"] == "failure"
    assert report["error_type"] == "RuntimeError"
    assert report["stages"][-1]["name"] == "fetch_sources"
    assert report["stages"][-1]["status"] == "failure"
