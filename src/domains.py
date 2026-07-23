"""Routing and isolated execution for parallel news-domain pipelines."""

from __future__ import annotations

import asyncio
from contextlib import nullcontext
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional

from .models import ContentItem, DomainConfig
from .performance import PerformanceRecorder


@dataclass
class DomainRoutingResult:
    """Items assigned to each enabled domain."""

    assignments: Dict[str, List[ContentItem]]
    routed_items: int
    multi_domain_items: int


class DomainRouter:
    """Route items by source category with multi-label support."""

    def __init__(self, domains: Dict[str, DomainConfig]):
        self.domains = {
            key: config for key, config in domains.items() if config.enabled
        }
        defaults = [
            key for key, config in self.domains.items() if config.default
        ]
        if len(defaults) != 1:
            raise ValueError(
                "domain routing requires exactly one enabled default domain"
            )
        self.default_domain = defaults[0]

    def route(self, items: List[ContentItem]) -> DomainRoutingResult:
        assignments = {key: [] for key in self.domains}
        multi_domain_items = 0

        for item in items:
            category = item.metadata.get("category")
            matches = [
                key
                for key, config in self.domains.items()
                if isinstance(category, str) and category in config.categories
            ]
            if not matches:
                matches = [self.default_domain]
            if len(matches) > 1:
                multi_domain_items += 1

            for key in matches:
                routed_item = item.model_copy(deep=True)
                routed_item.metadata["domain"] = key
                routed_item.metadata["routed_domains"] = list(matches)
                assignments[key].append(routed_item)

        return DomainRoutingResult(
            assignments=assignments,
            routed_items=sum(len(domain_items) for domain_items in assignments.values()),
            multi_domain_items=multi_domain_items,
        )


@dataclass
class DomainPipelineResult:
    """Serializable outcome of one isolated domain pipeline."""

    domain: str
    name: str
    status: str
    routed_items: int
    analyzed_items: int = 0
    threshold_items: int = 0
    selected_items: int = 0
    items: List[ContentItem] = field(default_factory=list)
    error_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "name": self.name,
            "status": self.status,
            "routed_items": self.routed_items,
            "analyzed_items": self.analyzed_items,
            "threshold_items": self.threshold_items,
            "selected_items": self.selected_items,
            "error_type": self.error_type,
        }


AnalyzeCallback = Callable[
    [List[ContentItem], str, DomainConfig],
    Awaitable[List[ContentItem]],
]
FilterCallback = Callable[[List[ContentItem], DomainConfig], Awaitable[Any]]
ExpandCallback = Callable[
    [List[ContentItem], str, DomainConfig],
    Awaitable[None],
]
BalanceCallback = Callable[[List[ContentItem], DomainConfig], Any]
EnrichCallback = Callable[
    [List[ContentItem], str, DomainConfig],
    Awaitable[None],
]


class DomainPipeline:
    """Run one domain while isolating failures from sibling domains."""

    def __init__(
        self,
        *,
        domain: str,
        config: DomainConfig,
        domain_semaphore: asyncio.Semaphore,
        analyze: AnalyzeCallback,
        filter_items: FilterCallback,
        expand_discussion: ExpandCallback,
        balance: BalanceCallback,
        enrich: EnrichCallback,
        recorder: Optional[PerformanceRecorder] = None,
    ) -> None:
        self.domain = domain
        self.config = config
        self.name = config.name or domain.replace("_", " ").title()
        self.domain_semaphore = domain_semaphore
        self.analyze = analyze
        self.filter_items = filter_items
        self.expand_discussion = expand_discussion
        self.balance = balance
        self.enrich = enrich
        self.recorder = recorder

    def _measure(self, name: str, *, input_items: Optional[int] = None):
        if self.recorder is None:
            return nullcontext()
        return self.recorder.domain_stage(
            self.domain,
            name,
            input_items=input_items,
        )

    async def run(self, items: List[ContentItem]) -> DomainPipelineResult:
        async with self.domain_semaphore:
            if not items:
                return DomainPipelineResult(
                    domain=self.domain,
                    name=self.name,
                    status="empty",
                    routed_items=0,
                )

            analyzed_count = 0
            threshold_count = 0
            selected_count = 0
            try:
                with self._measure(
                    "analyze_content",
                    input_items=len(items),
                ) as measurement:
                    analyzed = await self.analyze(items, self.domain, self.config)
                    analyzed_count = len(analyzed)
                    if measurement is not None:
                        measurement.set_result(output_items=analyzed_count)

                with self._measure(
                    "filter_and_topic_deduplicate",
                    input_items=analyzed_count,
                ) as measurement:
                    filtering_result = await self.filter_items(analyzed, self.config)
                    selected = filtering_result.items
                    selected_count = len(selected)
                    threshold_count = filtering_result.threshold_count
                    if measurement is not None:
                        measurement.set_result(
                            output_items=len(selected),
                            threshold_items=filtering_result.threshold_count,
                            topic_deduplicated_items=filtering_result.topic_dedup_count,
                            topic_duplicates_removed=filtering_result.topic_dedup_removed,
                        )

                with self._measure(
                    "expand_twitter_discussion",
                    input_items=len(selected),
                ) as measurement:
                    await self.expand_discussion(
                        selected,
                        self.domain,
                        self.config,
                    )
                    if measurement is not None:
                        measurement.set_result(output_items=len(selected))

                with self._measure(
                    "balance_digest",
                    input_items=len(selected),
                ) as measurement:
                    balanced = self.balance(selected, self.config)
                    selected = balanced.items
                    selected_count = len(selected)
                    if measurement is not None:
                        measurement.set_result(
                            output_items=len(selected),
                            enabled=balanced.enabled,
                            group_counts=balanced.group_counts,
                        )

                with self._measure(
                    "enrich_content",
                    input_items=len(selected),
                ) as measurement:
                    await self.enrich(selected, self.domain, self.config)
                    if measurement is not None:
                        measurement.set_result(output_items=len(selected))

                return DomainPipelineResult(
                    domain=self.domain,
                    name=self.name,
                    status="success",
                    routed_items=len(items),
                    analyzed_items=analyzed_count,
                    threshold_items=threshold_count,
                    selected_items=len(selected),
                    items=selected,
                )
            except Exception as exc:
                return DomainPipelineResult(
                    domain=self.domain,
                    name=self.name,
                    status="failure",
                    routed_items=len(items),
                    analyzed_items=analyzed_count,
                    threshold_items=threshold_count,
                    selected_items=selected_count,
                    error_type=type(exc).__name__,
                )
