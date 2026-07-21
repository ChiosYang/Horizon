"""Tests for stage-specific AI model routing."""

import asyncio
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

import src.orchestrator as orchestrator_module
from src.ai.enricher import ContentEnricher
from src.ai.client import _create_chained_client
from src.models import (
    AIConfig,
    AIProvider,
    AIStage,
    Config,
    ContentItem,
    FilteringConfig,
    SourceType,
    SourcesConfig,
)
from src.orchestrator import HorizonOrchestrator
from src.setup import ai_recommend


def _ai_config(**updates) -> AIConfig:
    values = {
        "provider": AIProvider.OPENAI,
        "model": "default-model",
        "api_key_env": "OPENAI_API_KEY",
        "base_url": "https://primary.example/v1",
        "temperature": 0.3,
        "analysis_concurrency": 3,
        "enrichment_concurrency": 2,
        "languages": ["en", "zh"],
    }
    values.update(updates)
    return AIConfig.model_validate(values)


def _item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url=f"https://example.com/{item_id}",
        content="content",
        published_at=datetime.now(timezone.utc),
    )


def test_stage_override_inherits_unspecified_default_fields() -> None:
    config = _ai_config(
        stages={
            "analysis": {
                "model": "fast-model",
                "temperature": 0.1,
            }
        }
    )

    resolved = config.for_stage(AIStage.ANALYSIS)

    assert resolved.model == "fast-model"
    assert resolved.temperature == 0.1
    assert resolved.provider == AIProvider.OPENAI
    assert resolved.api_key_env == "OPENAI_API_KEY"
    assert resolved.base_url == "https://primary.example/v1"
    assert resolved.analysis_concurrency == 3
    assert resolved.languages == ["en", "zh"]
    assert resolved.stages == {}


def test_switching_stage_provider_uses_that_provider_connection_defaults() -> None:
    config = _ai_config(
        provider_chain="openai,ollama",
        stages={
            "enrichment": {
                "provider": "deepseek",
                "model": "deepseek-v4-pro",
            }
        },
    )

    resolved = config.for_stage("enrichment")

    assert resolved.provider == AIProvider.DEEPSEEK
    assert resolved.model == "deepseek-v4-pro"
    assert resolved.api_key_env == "DEEPSEEK_API_KEY"
    assert resolved.base_url == "https://api.deepseek.com"
    assert resolved.provider_chain is None
    assert resolved.azure_endpoint_env is None
    assert resolved.api_version is None


def test_explicit_null_clears_inherited_optional_fields() -> None:
    config = _ai_config(
        provider_chain="openai,ollama",
        stages={
            "analysis": {
                "provider_chain": None,
                "base_url": None,
            }
        },
    )

    resolved = config.for_stage("analysis")

    assert resolved.provider_chain is None
    assert resolved.base_url is None


def test_unknown_stage_is_rejected_during_config_validation() -> None:
    with pytest.raises(ValidationError, match="unknown_stage"):
        _ai_config(stages={"unknown_stage": {"model": "model"}})


def test_stage_keys_serialize_as_json_strings() -> None:
    config = _ai_config(stages={"translation": {"model": "translator"}})

    payload = config.model_dump(mode="json")

    assert payload["stages"]["translation"]["model"] == "translator"


def test_stage_model_is_preserved_in_provider_chain_primary() -> None:
    config = _ai_config(
        provider_chain="openai,ollama",
        stages={"analysis": {"model": "analysis-model"}},
    )

    chained = _create_chained_client(config.for_stage("analysis"))

    assert chained.configs[0].provider == AIProvider.OPENAI
    assert chained.configs[0].model == "analysis-model"
    assert chained.configs[0].api_key_env == "OPENAI_API_KEY"
    assert chained.configs[1].provider == AIProvider.OLLAMA
    assert chained.configs[1].model == "llama3.1"


def test_content_enricher_uses_dedicated_translation_client() -> None:
    class DummyClient:
        def __init__(self, response: str):
            self.response = response
            self.calls = []

        async def complete(self, **kwargs):  # type: ignore[no-untyped-def]
            self.calls.append(kwargs)
            return self.response

    enrichment_client = DummyClient("unused")
    translation_client = DummyClient(
        '{"title_zh":"中文标题","summary_zh":"中文摘要"}'
    )
    item = _item("translation")
    enricher = ContentEnricher(
        enrichment_client,  # type: ignore[arg-type]
        translation_client=translation_client,  # type: ignore[arg-type]
    )

    asyncio.run(enricher._translate_item(item))

    assert enrichment_client.calls == []
    assert len(translation_client.calls) == 1
    assert item.metadata["title_zh"] == "中文标题"
    assert item.metadata["detailed_summary_zh"] == "中文摘要"


def test_orchestrator_routes_each_ai_stage(monkeypatch) -> None:
    ai = _ai_config(
        stages={
            "analysis": {"model": "analysis-model"},
            "deduplication": {"model": "dedup-model"},
            "enrichment": {"model": "enrichment-model"},
            "translation": {"model": "translation-model"},
        }
    )
    config = Config(
        ai=ai,
        sources=SourcesConfig(),
        filtering=FilteringConfig(),
    )
    created_configs = []
    enrichment_clients = []

    class DummyClient:
        def __init__(self, client_config: AIConfig):
            self.config = client_config

        async def complete(self, **kwargs):  # type: ignore[no-untyped-def]
            return '{"duplicates":[]}'

    class DummyAnalyzer:
        def __init__(self, client):  # type: ignore[no-untyped-def]
            self.client = client

        async def analyze_batch(self, items):  # type: ignore[no-untyped-def]
            return items

    class DummyEnricher:
        def __init__(self, client, translation_client=None):  # type: ignore[no-untyped-def]
            enrichment_clients.extend([client, translation_client])

        async def enrich_batch(self, items):  # type: ignore[no-untyped-def]
            return None

    def create_client(client_config: AIConfig) -> DummyClient:
        created_configs.append(client_config)
        return DummyClient(client_config)

    monkeypatch.setattr(orchestrator_module, "create_ai_client", create_client)
    monkeypatch.setattr(orchestrator_module, "ContentAnalyzer", DummyAnalyzer)
    monkeypatch.setattr(orchestrator_module, "ContentEnricher", DummyEnricher)

    orchestrator = HorizonOrchestrator(config, storage=object())  # type: ignore[arg-type]
    items = [_item("one"), _item("two")]
    asyncio.run(orchestrator._analyze_content(items))
    asyncio.run(orchestrator.merge_topic_duplicates(items, log=False))
    asyncio.run(orchestrator._enrich_important_items(items))

    assert [config.model for config in created_configs] == [
        "analysis-model",
        "dedup-model",
        "enrichment-model",
        "translation-model",
    ]
    assert [client.config.model for client in enrichment_clients] == [
        "enrichment-model",
        "translation-model",
    ]


def test_source_recommendation_uses_its_stage_config(monkeypatch) -> None:
    ai = _ai_config(
        stages={"source_recommendation": {"model": "recommendation-model"}}
    )
    captured = []

    class DummyClient:
        async def complete(self, **kwargs):  # type: ignore[no-untyped-def]
            return '{"sources":[]}'

    def create_client(config: AIConfig) -> DummyClient:
        captured.append(config)
        return DummyClient()

    monkeypatch.setattr(ai_recommend, "create_ai_client", create_client)

    result = asyncio.run(ai_recommend.get_ai_recommendations(ai, "AI", []))

    assert result == []
    assert captured[0].model == "recommendation-model"
