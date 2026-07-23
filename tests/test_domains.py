import asyncio
import json
import threading
import time
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.ai.analyzer import ContentAnalyzer
from src.ai.enricher import ContentEnricher
from src.domains import DomainRouter
from src.models import (
    AIConfig,
    Config,
    ContentItem,
    DomainConfig,
    FilteringConfig,
    SourceType,
    SourcesConfig,
)
from src.orchestrator import HorizonOrchestrator
from src.storage.manager import StorageManager


def _item(item_id: str, category: str | None) -> ContentItem:
    metadata = {"category": category} if category is not None else {}
    return ContentItem(
        id=f"rss:{item_id}",
        source_type=SourceType.RSS,
        title=item_id,
        url=f"https://example.com/{item_id}",
        published_at=datetime.now(timezone.utc),
        metadata=metadata,
    )


def _config(
    domains: dict[str, DomainConfig],
    *,
    domain_concurrency: int = 2,
) -> Config:
    return Config(
        ai=AIConfig(
            provider="openai",
            model="test",
            api_key_env="TEST_API_KEY",
            languages=[],
            analysis_concurrency=4,
            enrichment_concurrency=3,
            total_concurrency=2,
            search_concurrency=1,
        ),
        sources=SourcesConfig(),
        filtering=FilteringConfig(ai_score_threshold=7.0),
        domains=domains,
        domain_concurrency=domain_concurrency,
    )


def test_configured_domains_require_one_enabled_default() -> None:
    domains = {
        "ai": DomainConfig(categories=["ai-news"]),
        "economy": DomainConfig(categories=["finance"]),
    }

    with pytest.raises(ValidationError, match="exactly one enabled default"):
        _config(domains)

    domains["general"] = DomainConfig(default=True)
    config = _config(domains)

    assert config.domains["general"].default is True


def test_config_rejects_unsafe_domain_keys() -> None:
    with pytest.raises(ValidationError, match="invalid domain key"):
        _config({"../outside": DomainConfig(default=True)})


def test_router_supports_multi_label_and_default_routing_with_copies() -> None:
    router = DomainRouter(
        {
            "ai": DomainConfig(categories=["ai-news"]),
            "technology": DomainConfig(categories=["ai-news", "developer"]),
            "general": DomainConfig(default=True),
        }
    )
    ai_item = _item("shared", "ai-news")
    unmatched_item = _item("unmatched", None)

    result = router.route([ai_item, unmatched_item])

    assert result.routed_items == 3
    assert result.multi_domain_items == 1
    assert [item.id for item in result.assignments["ai"]] == [ai_item.id]
    assert [item.id for item in result.assignments["technology"]] == [ai_item.id]
    assert [item.id for item in result.assignments["general"]] == [
        unmatched_item.id
    ]
    assert result.assignments["ai"][0] is not result.assignments["technology"][0]
    result.assignments["ai"][0].metadata["mutated"] = True
    assert "mutated" not in result.assignments["technology"][0].metadata
    assert "domain" not in ai_item.metadata


def test_domain_threshold_and_item_cap_override_global_filtering(tmp_path) -> None:
    config = _config({"general": DomainConfig(default=True)})
    orchestrator = HorizonOrchestrator(
        config,
        StorageManager(data_dir=str(tmp_path / "data")),
    )
    higher = _item("higher", "world")
    lower = _item("lower", "world")
    higher.ai_score = 9.0
    lower.ai_score = 8.0
    domain = DomainConfig(
        default=True,
        score_threshold=8.5,
        max_items=1,
    )

    filtered = asyncio.run(
        orchestrator._filter_domain_items([lower, higher], domain)
    )
    balanced = orchestrator._balance_domain_items(
        [lower, higher],
        domain,
    )

    assert [item.id for item in filtered.items] == [higher.id]
    assert [item.id for item in balanced.items] == [higher.id]


def test_parallel_domain_run_respects_domain_concurrency_and_records_metrics(
    tmp_path,
    monkeypatch,
) -> None:
    config = _config(
        {
            "ai": DomainConfig(name="AI News", categories=["ai-news"]),
            "economy": DomainConfig(name="Economy", categories=["finance"]),
            "general": DomainConfig(name="General", default=True),
        },
        domain_concurrency=2,
    )
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    orchestrator = HorizonOrchestrator(config, storage)
    items = [
        _item("ai", "ai-news"),
        _item("economy", "finance"),
        _item("general", "world"),
    ]
    active = 0
    max_active = 0

    async def fetch_all_sources(since):  # type: ignore[no-untyped-def]
        return items

    async def analyze_content(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        nonlocal active, max_active
        active += 1
        max_active = max(max_active, active)
        await asyncio.sleep(0.03)
        for item in input_items:
            item.ai_score = 9.0
        active -= 1
        return input_items

    async def expand_discussion(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        return None

    async def enrich_items(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        return None

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)
    monkeypatch.setattr(orchestrator, "_analyze_content", analyze_content)
    monkeypatch.setattr(
        orchestrator,
        "_expand_twitter_discussion",
        expand_discussion,
    )
    monkeypatch.setattr(
        orchestrator,
        "_enrich_important_items",
        enrich_items,
    )
    monkeypatch.chdir(tmp_path)

    asyncio.run(orchestrator.run())

    assert max_active == 2
    assert {result.status for result in orchestrator.last_domain_results} == {
        "success"
    }
    assert all(
        result.selected_items == 1
        for result in orchestrator.last_domain_results
    )
    assert all("domain" not in item.metadata for item in items)

    report_path = next(storage.metrics_dir.glob("horizon-performance-*.json"))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "success"
    assert {result["domain"] for result in report["domains"]} == {
        "ai",
        "economy",
        "general",
    }
    metric_domains = {
        metric["attributes"]["domain"]
        for metric in report["domain_stages"]
    }
    assert metric_domains == {"ai", "economy", "general"}


def test_domain_failure_is_isolated_from_successful_sibling(
    tmp_path,
    monkeypatch,
) -> None:
    config = _config(
        {
            "ai": DomainConfig(categories=["ai-news"]),
            "general": DomainConfig(default=True),
        }
    )
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    orchestrator = HorizonOrchestrator(config, storage)

    async def fetch_all_sources(since):  # type: ignore[no-untyped-def]
        return [_item("ai", "ai-news"), _item("general", "world")]

    async def analyze_content(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        if domain_key == "ai":
            raise TimeoutError("AI domain timed out")
        input_items[0].ai_score = 9.0
        return input_items

    async def no_op(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        return None

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)
    monkeypatch.setattr(orchestrator, "_analyze_content", analyze_content)
    monkeypatch.setattr(orchestrator, "_expand_twitter_discussion", no_op)
    monkeypatch.setattr(orchestrator, "_enrich_important_items", no_op)
    monkeypatch.chdir(tmp_path)

    asyncio.run(orchestrator.run())

    statuses = {
        result.domain: result.status for result in orchestrator.last_domain_results
    }
    assert statuses == {"ai": "failure", "general": "success"}
    assert orchestrator.last_performance_report is not None
    assert orchestrator.last_performance_report["status"] == "partial_success"
    process_stage = next(
        stage
        for stage in orchestrator.last_performance_report["stages"]
        if stage["name"] == "process_domains"
    )
    assert process_stage["status"] == "partial_failure"


def test_domain_run_writes_independent_digest_for_each_domain(
    tmp_path,
    monkeypatch,
) -> None:
    config = _config(
        {
            "ai": DomainConfig(name="AI News", categories=["ai-news"]),
            "general": DomainConfig(name="General News", default=True),
        }
    )
    config.ai.languages = ["en"]
    storage = StorageManager(data_dir=str(tmp_path / "data"))
    orchestrator = HorizonOrchestrator(config, storage)

    async def fetch_all_sources(since):  # type: ignore[no-untyped-def]
        return [_item("ai", "ai-news")]

    async def analyze_content(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        input_items[0].ai_score = 9.0
        return input_items

    async def no_op(  # type: ignore[no-untyped-def]
        input_items,
        domain_key=None,
        domain_config=None,
    ):
        return None

    monkeypatch.setattr(orchestrator, "fetch_all_sources", fetch_all_sources)
    monkeypatch.setattr(orchestrator, "_analyze_content", analyze_content)
    monkeypatch.setattr(orchestrator, "_expand_twitter_discussion", no_op)
    monkeypatch.setattr(orchestrator, "_enrich_important_items", no_op)
    monkeypatch.chdir(tmp_path)

    asyncio.run(orchestrator.run())

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ai_path = storage.summaries_dir / f"horizon-{today}-ai-en.md"
    general_path = storage.summaries_dir / f"horizon-{today}-general-en.md"
    assert ai_path.read_text(encoding="utf-8").startswith(f"# AI News - {today}")
    assert general_path.read_text(encoding="utf-8").startswith(
        f"# General News - {today}"
    )
    statuses = {
        result.domain: result.status for result in orchestrator.last_domain_results
    }
    assert statuses == {"ai": "success", "general": "empty"}


def test_analyzers_share_cross_domain_ai_concurrency_budget() -> None:
    class Client:
        def __init__(self) -> None:
            self.config = type("Config", (), {"analysis_concurrency": 4})()
            self.active = 0
            self.max_active = 0
            self.system_prompts: list[str] = []

        async def complete(self, **kwargs):  # type: ignore[no-untyped-def]
            self.system_prompts.append(kwargs["system"])
            self.active += 1
            self.max_active = max(self.max_active, self.active)
            await asyncio.sleep(0.02)
            self.active -= 1
            return '{"score": 9, "reason": "important", "summary": "ok", "tags": []}'

    async def run() -> int:
        client = Client()
        shared_semaphore = asyncio.Semaphore(1)
        first = ContentAnalyzer(
            client,  # type: ignore[arg-type]
            semaphore=shared_semaphore,
            domain_guidance="Focus on AI model releases.",
            show_progress=False,
        )
        second = ContentAnalyzer(
            client,  # type: ignore[arg-type]
            semaphore=shared_semaphore,
            domain_guidance="Focus on market impact.",
            show_progress=False,
        )
        await asyncio.gather(
            first.analyze_batch([_item("first", "ai-news")]),
            second.analyze_batch([_item("second", "finance")]),
        )
        assert any("AI model releases" in prompt for prompt in client.system_prompts)
        assert any("market impact" in prompt for prompt in client.system_prompts)
        return client.max_active

    assert asyncio.run(run()) == 1


def test_enrichers_share_cross_domain_search_concurrency_budget(
    monkeypatch,
) -> None:
    class Search:
        active = 0
        max_active = 0
        lock = threading.Lock()

        def text(self, query, max_results=3):  # type: ignore[no-untyped-def]
            with self.lock:
                type(self).active += 1
                type(self).max_active = max(
                    type(self).max_active,
                    type(self).active,
                )
            time.sleep(0.02)
            with self.lock:
                type(self).active -= 1
            return []

    monkeypatch.setattr("src.ai.enricher.DDGS", Search)

    async def run() -> int:
        shared_semaphore = asyncio.Semaphore(1)
        first = ContentEnricher(
            object(),  # type: ignore[arg-type]
            search_semaphore=shared_semaphore,
            show_progress=False,
        )
        second = ContentEnricher(
            object(),  # type: ignore[arg-type]
            search_semaphore=shared_semaphore,
            show_progress=False,
        )
        await asyncio.gather(
            first._web_search("first"),
            second._web_search("second"),
        )
        return Search.max_active

    assert asyncio.run(run()) == 1


def test_domain_summary_filename_isolated_and_safe(tmp_path) -> None:
    storage = StorageManager(data_dir=str(tmp_path / "data"))

    path = storage.save_daily_summary(
        "2026-07-22",
        "# AI News",
        language="zh",
        domain="ai",
    )

    assert path.name == "horizon-2026-07-22-ai-zh.md"
    with pytest.raises(ValueError, match="Invalid summary domain"):
        storage.save_daily_summary(
            "2026-07-22",
            "unsafe",
            domain="../outside",
        )
