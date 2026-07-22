"""Main orchestrator coordinating the entire workflow."""

import asyncio
import json
from collections import defaultdict
from contextlib import nullcontext
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Literal, Optional
from urllib.parse import unquote_plus, urlsplit
import httpx
from rich.console import Console

from .models import AIStage, Config, ContentItem, DomainConfig, FilteringConfig
from .domains import (
    DomainPipeline,
    DomainPipelineResult,
    DomainRouter,
)
from .storage.manager import StorageManager, safe_output_path
from .services.email import EmailManager
from .services.webhook import WebhookNotifier
from .scrapers.github import GitHubScraper
from .scrapers.hackernews import HackerNewsScraper
from .scrapers.rss import RSSScraper
from .scrapers.reddit import RedditScraper
from .scrapers.telegram import TelegramScraper
from .scrapers.twitter import TwitterScraper
from .scrapers.twitter_playwright import TwitterPlaywrightScraper
from .scrapers.openbb import OpenBBScraper
from .scrapers.google_news import GoogleNewsScraper
from .ai.client import create_ai_client
from .ai.analyzer import ContentAnalyzer
from .ai.summarizer import DailySummarizer
from .ai.enricher import ContentEnricher
from .ai.tokens import get_usage_snapshot
from .performance import PerformanceRecorder


_TRACKING_QUERY_PARAMETERS = {
    "_ga",
    "dclid",
    "fbclid",
    "gclid",
    "igshid",
    "li_fat_id",
    "mc_cid",
    "mc_eid",
    "msclkid",
    "ttclid",
    "twclid",
    "vero_id",
}


def _deduplication_url_key(url: str) -> tuple[str, str, str, str, Optional[int], str, str]:
    """Return a conservative URL identity key for cross-source deduplication."""
    parsed = urlsplit(url)
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    port = parsed.port
    if (scheme, port) in {("http", 80), ("https", 443)}:
        port = None

    path = parsed.path.rstrip("/") or "/"
    query_parts = []
    for part in parsed.query.split("&") if parsed.query else []:
        name = unquote_plus(part.partition("=")[0]).lower()
        if name.startswith("utm_") or name in _TRACKING_QUERY_PARAMETERS:
            continue
        query_parts.append(part)

    return (
        scheme,
        parsed.username or "",
        parsed.password or "",
        host,
        port,
        path,
        "&".join(query_parts),
    )


@dataclass
class BalancedDigestResult:
    """Items and selection statistics from balanced digest filtering."""

    items: List[ContentItem]
    enabled: bool = False
    group_counts: Dict[str, int] = field(default_factory=dict)
    group_limits: Dict[str, Optional[int]] = field(default_factory=dict)
    duplicate_categories: List[str] = field(default_factory=list)


@dataclass
class FilteringPipelineResult:
    """Items and statistics from score, topic, and digest filtering."""

    items: List[ContentItem]
    threshold_count: int
    topic_dedup_count: int
    topic_dedup_removed: int
    balanced_digest: BalancedDigestResult


@dataclass
class SourceFetchOutcome:
    """Result of fetching one configured source."""

    source_name: str
    status: Literal["success", "empty", "failure"]
    items: List[ContentItem] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "source": self.source_name,
            "status": self.status,
            "item_count": len(self.items),
        }
        if self.error is not None:
            result["error"] = self.error
        return result


@dataclass
class FetchReport:
    """Aggregate diagnostics for one fetch across configured sources."""

    outcomes: List[SourceFetchOutcome] = field(default_factory=list)

    @property
    def status(self) -> Literal["not_attempted", "success", "partial_failure", "failure"]:
        if not self.outcomes:
            return "not_attempted"
        if self.failed_count == len(self.outcomes):
            return "failure"
        if self.failed_count:
            return "partial_failure"
        return "success"

    @property
    def failed_count(self) -> int:
        return sum(outcome.status == "failure" for outcome in self.outcomes)

    @property
    def all_failed(self) -> bool:
        return bool(self.outcomes) and self.failed_count == len(self.outcomes)

    def failure_message(self) -> str:
        failures = "; ".join(
            f"{outcome.source_name}: {outcome.error or 'unknown error'}"
            for outcome in self.outcomes
            if outcome.status == "failure"
        )
        return f"All {len(self.outcomes)} attempted sources failed ({failures})"

    def to_dict(self) -> Dict[str, object]:
        return {
            "status": self.status,
            "attempted": len(self.outcomes),
            "successful": len(self.outcomes) - self.failed_count,
            "empty": sum(outcome.status == "empty" for outcome in self.outcomes),
            "failed": self.failed_count,
            "item_count": sum(len(outcome.items) for outcome in self.outcomes),
            "sources": [outcome.to_dict() for outcome in self.outcomes],
        }


class HorizonOrchestrator:
    """Orchestrates the complete workflow for content aggregation and analysis."""

    def __init__(self, config: Config, storage: StorageManager):
        """Initialize orchestrator.

        Args:
            config: Application configuration
            storage: Storage manager
        """
        self.config = config
        self.storage = storage
        self.console = Console()
        self.email_manager = EmailManager(config.email, console=self.console) if config.email else None
        self.webhook_notifier = (
            WebhookNotifier(config.webhook, console=self.console)
            if config.webhook and config.webhook.enabled
            else None
        )
        self.last_fetch_report: Optional[FetchReport] = None
        self.last_performance_report: Optional[Dict[str, object]] = None
        self.last_domain_results: List[DomainPipelineResult] = []
        self._performance_recorder: Optional[PerformanceRecorder] = None
        self._domain_ai_semaphore: Optional[asyncio.Semaphore] = None
        self._domain_search_semaphore: Optional[asyncio.Semaphore] = None

    async def run(self, force_hours: int = None) -> None:
        """Execute the complete workflow.

        Args:
            force_hours: Optional override for time window in hours
        """
        recorder = PerformanceRecorder()
        self._performance_recorder = recorder
        self.last_domain_results = []
        run_status = "success"
        run_error_type: Optional[str] = None

        self.console.print("[bold cyan]🌅 Horizon - Starting aggregation...[/bold cyan]\n")

        try:
            # 1. Determine time window
            with recorder.stage("determine_time_window") as measurement:
                since = self._determine_time_window(force_hours)
                measurement.set_result(
                    since=since.isoformat(),
                    force_hours=force_hours,
                )
            self.console.print(f"📅 Fetching content since: {since.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # 2. Fetch content from all sources
            with recorder.stage("fetch_sources") as measurement:
                all_items = await self.fetch_all_sources(since)
                fetch_status = (
                    self.last_fetch_report.status
                    if self.last_fetch_report is not None
                    else "success"
                )
                measurement.set_result(
                    status=fetch_status,
                    output_items=len(all_items),
                )
            self.console.print(f"📥 Fetched {len(all_items)} items from all sources\n")

            if self.last_fetch_report and self.last_fetch_report.all_failed:
                raise RuntimeError(self.last_fetch_report.failure_message())

            if not all_items:
                run_status = "no_content"
                self.console.print("[yellow]No new content found. Exiting.[/yellow]")
                return

            # 3. Merge cross-source duplicates (same URL from different sources)
            with recorder.stage(
                "merge_cross_source_duplicates",
                input_items=len(all_items),
            ) as measurement:
                merged_items = self.merge_cross_source_duplicates(all_items)
                measurement.set_result(output_items=len(merged_items))
            if len(merged_items) < len(all_items):
                self.console.print(
                    f"🔗 Merged {len(all_items) - len(merged_items)} cross-source duplicates "
                    f"→ {len(merged_items)} unique items\n"
                )

            if self.config.domains:
                with recorder.stage(
                    "route_domains",
                    input_items=len(merged_items),
                ) as measurement:
                    routing = DomainRouter(self.config.domains).route(merged_items)
                    measurement.set_result(
                        output_items=routing.routed_items,
                        domains=len(routing.assignments),
                        multi_domain_items=routing.multi_domain_items,
                    )
                self.console.print(
                    f"🧭 Routed {len(merged_items)} unique items into "
                    f"{len(routing.assignments)} domains "
                    f"({routing.routed_items} assignments)\n"
                )

                with recorder.stage(
                    "process_domains",
                    input_items=routing.routed_items,
                ) as measurement:
                    domain_results = await self._run_domain_pipelines(
                        routing.assignments,
                        recorder,
                    )
                    self.last_domain_results = domain_results
                    processing_failures = sum(
                        result.status == "failure" for result in domain_results
                    )
                    if processing_failures == len(domain_results):
                        domain_status = "failure"
                    elif processing_failures:
                        domain_status = "partial_failure"
                    else:
                        domain_status = "success"
                    measurement.set_result(
                        status=domain_status,
                        output_items=sum(
                            result.selected_items
                            for result in domain_results
                            if result.status != "failure"
                        ),
                        succeeded=len(domain_results) - processing_failures,
                        failed=processing_failures,
                    )

                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                await self._publish_domain_results(
                    domain_results,
                    today=today,
                    all_items_count=len(all_items),
                    recorder=recorder,
                )

                failures = [
                    result for result in domain_results
                    if result.status == "failure"
                ]
                if len(failures) == len(domain_results):
                    failed_names = ", ".join(result.domain for result in failures)
                    raise RuntimeError(
                        f"All configured domain pipelines failed: {failed_names}"
                    )
                if failures:
                    run_status = "partial_success"
                    self.console.print(
                        f"[yellow]⚠️  Horizon completed with "
                        f"{len(failures)} failed domain(s).[/yellow]"
                    )
                else:
                    self.console.print(
                        "[bold green]✅ Horizon completed all domains successfully!"
                        "[/bold green]"
                    )
                self._print_token_usage()
                return

            # 4. Analyze with AI
            with recorder.stage(
                "analyze_content",
                input_items=len(merged_items),
            ) as measurement:
                analyzed_items = await self._analyze_content(merged_items)
                measurement.set_result(output_items=len(analyzed_items))
            self.console.print(f"🤖 Analyzed {len(analyzed_items)} items with AI\n")

            # 5. Filter, deduplicate, and balance the digest
            with recorder.stage(
                "filter_and_topic_deduplicate",
                input_items=len(analyzed_items),
            ) as measurement:
                filtering_result = await self.filter_items(
                    analyzed_items,
                    apply_balance=False,
                )
                measurement.set_result(
                    output_items=len(filtering_result.items),
                    threshold_items=filtering_result.threshold_count,
                    topic_deduplicated_items=filtering_result.topic_dedup_count,
                    topic_duplicates_removed=filtering_result.topic_dedup_removed,
                )
            important_items = filtering_result.items

            # 5.5 Optional second-stage Twitter reply expansion + targeted re-analysis
            with recorder.stage(
                "expand_twitter_discussion",
                input_items=len(important_items),
            ) as measurement:
                await self._expand_twitter_discussion(important_items)
                measurement.set_result(output_items=len(important_items))

            # 5.6 Apply digest limits after any targeted re-analysis changes scores.
            with recorder.stage(
                "balance_digest",
                input_items=len(important_items),
            ) as measurement:
                balanced_digest = self.apply_balanced_digest(important_items)
                important_items = balanced_digest.items
                measurement.set_result(
                    output_items=len(important_items),
                    enabled=balanced_digest.enabled,
                    group_counts=balanced_digest.group_counts,
                )

            # Show per-sub-source selection breakdown
            selected_counts: Dict[str, int] = defaultdict(int)
            for item in important_items:
                key = f"{item.source_type.value}/{self._sub_source_label(item)}"
                selected_counts[key] += 1
            for source_key, count in sorted(selected_counts.items()):
                self.console.print(f"      • {source_key}: {count}")
            self.console.print("")

            # 6. Search related stories + enrich with background knowledge (2nd AI pass)
            with recorder.stage(
                "enrich_content",
                input_items=len(important_items),
            ) as measurement:
                await self._enrich_important_items(important_items)
                measurement.set_result(output_items=len(important_items))

            # 7. Generate and save daily summaries for each configured language
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            for lang in self.config.ai.languages:
                summarizer = DailySummarizer()
                with recorder.stage(
                    "generate_summary",
                    input_items=len(important_items),
                    attributes={"language": lang},
                ) as measurement:
                    summary = await summarizer.generate_summary(
                        important_items,
                        today,
                        len(all_items),
                        language=lang,
                    )
                    measurement.set_result(
                        output_items=len(important_items),
                        summary_characters=len(summary),
                    )

                # Save to data/summaries/
                with recorder.stage(
                    "save_summary",
                    attributes={"language": lang},
                ):
                    summary_path = self.storage.save_daily_summary(
                        today,
                        summary,
                        language=lang,
                    )
                self.console.print(f"💾 Saved {lang.upper()} summary to: {summary_path}\n")

                # Copy to docs/ only when GitHub Pages publishing is enabled.
                with recorder.stage(
                    "publish_github_pages",
                    attributes={"language": lang},
                ) as measurement:
                    try:
                        dest_path = self._publish_github_pages_summary(
                            summary=summary,
                            date=today,
                            language=lang,
                        )
                    except Exception as e:
                        measurement.mark_failure(e)
                        self.console.print(
                            f"[yellow]⚠️  Failed to copy {lang.upper()} summary "
                            f"to docs/: {e}[/yellow]\n"
                        )
                    else:
                        measurement.set_result(
                            status="success" if dest_path is not None else "skipped"
                        )
                        if dest_path is not None:
                            self.console.print(
                                f"📄 Copied {lang.upper()} summary to GitHub Pages: "
                                f"{dest_path}\n"
                            )

                # Send email if configured
                if self.email_manager and self.config.email and self.config.email.enabled:
                    self.console.print(f"📧 Sending {lang.upper()} email summary...")
                    subject = f"Horizon Summary ({lang.upper()}) - {today}"
                    with recorder.stage(
                        "send_email",
                        attributes={"language": lang},
                    ):
                        self.email_manager.send_daily_summary(summary, subject)

                # Send webhook notification if configured
                if self.webhook_notifier:
                    with recorder.stage(
                        "send_webhook",
                        input_items=len(important_items),
                        attributes={"language": lang},
                    ) as measurement:
                        await self.webhook_notifier.send_daily_summary(
                            summary=summary,
                            important_items=important_items,
                            all_items_count=len(all_items),
                            date=today,
                            lang=lang,
                            summarizer=summarizer,
                        )
                        measurement.set_result(output_items=len(important_items))

            self.console.print("[bold green]✅ Horizon completed successfully![/bold green]")
            self._print_token_usage()

        except Exception as e:
            run_status = "failure"
            run_error_type = type(e).__name__
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")

            # Send webhook failure notification if configured
            if self.webhook_notifier:
                with recorder.stage("send_failure_webhook"):
                    await self.webhook_notifier.send_failure(
                        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        error_message=str(e),
                    )

            raise
        finally:
            recorder.finish(run_status, error_type=run_error_type)
            report = recorder.to_dict()
            if self.last_domain_results:
                report["domains"] = [
                    result.to_dict() for result in self.last_domain_results
                ]
            self.last_performance_report = report
            self._print_performance_summary(recorder)
            self._save_performance_report(recorder, report)
            self._performance_recorder = None
            self._domain_ai_semaphore = None
            self._domain_search_semaphore = None

    async def _run_domain_pipelines(
        self,
        assignments: Dict[str, List[ContentItem]],
        recorder: PerformanceRecorder,
    ) -> List[DomainPipelineResult]:
        """Run enabled domain pipelines concurrently with shared budgets."""
        total_ai_concurrency = self.config.ai.total_concurrency or max(
            self.config.ai.analysis_concurrency,
            self.config.ai.enrichment_concurrency,
        )
        self._domain_ai_semaphore = asyncio.Semaphore(total_ai_concurrency)
        self._domain_search_semaphore = asyncio.Semaphore(
            self.config.ai.search_concurrency
        )
        domain_semaphore = asyncio.Semaphore(self.config.domain_concurrency)

        pipelines = [
            DomainPipeline(
                domain=domain,
                config=domain_config,
                domain_semaphore=domain_semaphore,
                analyze=self._analyze_content,
                filter_items=self._filter_domain_items,
                expand_discussion=self._expand_twitter_discussion,
                balance=self._balance_domain_items,
                enrich=self._enrich_important_items,
                recorder=recorder,
            )
            for domain, domain_config in self.config.domains.items()
            if domain_config.enabled
        ]
        results = await asyncio.gather(
            *(
                pipeline.run(assignments.get(pipeline.domain, []))
                for pipeline in pipelines
            )
        )

        for result in results:
            if result.status == "failure":
                self.console.print(
                    f"   [red]✗ {result.name}: failed "
                    f"({result.error_type or 'unknown error'})[/red]"
                )
            else:
                self.console.print(
                    f"   [green]✓ {result.name}: "
                    f"{result.routed_items} routed → "
                    f"{result.selected_items} selected[/green]"
                )
        self.console.print("")
        return results

    async def _filter_domain_items(
        self,
        items: List[ContentItem],
        domain_config: DomainConfig,
    ) -> FilteringPipelineResult:
        threshold = (
            domain_config.score_threshold
            if domain_config.score_threshold is not None
            else self.config.filtering.ai_score_threshold
        )
        return await self.filter_items(
            items,
            threshold=threshold,
            apply_balance=False,
            log=False,
            ai_semaphore=self._domain_ai_semaphore,
        )

    def _balance_domain_items(
        self,
        items: List[ContentItem],
        domain_config: DomainConfig,
    ) -> BalancedDigestResult:
        max_items = (
            domain_config.max_items
            if domain_config.max_items is not None
            else self.config.filtering.max_items
        )
        filtering: FilteringConfig = self.config.filtering.model_copy(
            update={"max_items": max_items}
        )
        return self.apply_balanced_digest(
            items,
            filtering=filtering,
            log=False,
        )

    async def _publish_domain_results(
        self,
        results: List[DomainPipelineResult],
        *,
        today: str,
        all_items_count: int,
        recorder: PerformanceRecorder,
    ) -> None:
        """Generate and publish one independent digest per successful domain."""

        publish_semaphore = asyncio.Semaphore(self.config.domain_concurrency)

        async def publish_one(result: DomainPipelineResult) -> None:
            if result.status == "failure":
                return

            domain_config = self.config.domains[result.domain]
            languages = domain_config.languages or self.config.ai.languages
            try:
                for language in languages:
                    summarizer = DailySummarizer()
                    attributes = {"language": language}
                    with recorder.domain_stage(
                        result.domain,
                        "generate_summary",
                        input_items=len(result.items),
                        attributes=attributes,
                    ) as measurement:
                        summary = await summarizer.generate_summary(
                            result.items,
                            today,
                            all_items_count,
                            language=language,
                            heading=result.name,
                        )
                        measurement.set_result(
                            output_items=len(result.items),
                            summary_characters=len(summary),
                        )

                    with recorder.domain_stage(
                        result.domain,
                        "save_summary",
                        attributes=attributes,
                    ):
                        summary_path = self.storage.save_daily_summary(
                            today,
                            summary,
                            language=language,
                            domain=result.domain,
                        )
                    self.console.print(
                        f"💾 Saved {result.name} {language.upper()} summary to: "
                        f"{summary_path}"
                    )

                    with recorder.domain_stage(
                        result.domain,
                        "publish_github_pages",
                        attributes=attributes,
                    ) as measurement:
                        try:
                            dest_path = self._publish_github_pages_summary(
                                summary=summary,
                                date=today,
                                language=language,
                                domain=result.domain,
                                domain_name=result.name,
                            )
                        except Exception as exc:
                            measurement.mark_failure(exc)
                            self.console.print(
                                f"[yellow]⚠️  Failed to copy {result.name} "
                                f"{language.upper()} summary to docs/: {exc}[/yellow]"
                            )
                        else:
                            measurement.set_result(
                                status=(
                                    "success" if dest_path is not None else "skipped"
                                )
                            )

                    if (
                        self.email_manager
                        and self.config.email
                        and self.config.email.enabled
                    ):
                        subject = (
                            f"Horizon {result.name} Summary "
                            f"({language.upper()}) - {today}"
                        )
                        with recorder.domain_stage(
                            result.domain,
                            "send_email",
                            attributes=attributes,
                        ):
                            await asyncio.to_thread(
                                self.email_manager.send_daily_summary,
                                summary,
                                subject,
                            )

                    if self.webhook_notifier:
                        with recorder.domain_stage(
                            result.domain,
                            "send_webhook",
                            input_items=len(result.items),
                            attributes=attributes,
                        ) as measurement:
                            await self.webhook_notifier.send_daily_summary(
                                summary=summary,
                                important_items=result.items,
                                all_items_count=all_items_count,
                                date=today,
                                lang=language,
                                summarizer=summarizer,
                                domain_name=result.name,
                            )
                            measurement.set_result(output_items=len(result.items))
            except Exception as exc:
                result.status = "failure"
                result.error_type = type(exc).__name__
                self.console.print(
                    f"[red]✗ Failed to publish {result.name}: "
                    f"{type(exc).__name__}: {exc}[/red]"
                )

        async def publish(result: DomainPipelineResult) -> None:
            async with publish_semaphore:
                await publish_one(result)

        await asyncio.gather(*(publish(result) for result in results))
        self.console.print("")

    def _print_token_usage(self) -> None:
        usage = get_usage_snapshot()
        if usage.total_tokens <= 0:
            return
        self.console.print(
            f"\n🧮 Token usage this run: "
            f"{usage.total_tokens} tokens "
            f"(input: {usage.total_input_tokens}, "
            f"output: {usage.total_output_tokens})"
        )
        for provider, provider_usage in sorted(usage.per_provider.items()):
            if provider_usage.total <= 0:
                continue
            self.console.print(
                f"   • {provider}: {provider_usage.total} tokens "
                f"(in: {provider_usage.input_tokens}, "
                f"out: {provider_usage.output_tokens})"
            )

    def _print_performance_summary(self, recorder: PerformanceRecorder) -> None:
        """Print a concise stage timing summary for the completed run."""

        self.console.print("\n[bold cyan]⏱ Performance summary[/bold cyan]")
        for metric in recorder.stages:
            count_label = ""
            if metric.input_items is not None or metric.output_items is not None:
                input_label = "-" if metric.input_items is None else metric.input_items
                output_label = "-" if metric.output_items is None else metric.output_items
                count_label = f" | items {input_label}→{output_label}"
            token_label = ""
            if metric.tokens.total_tokens:
                token_label = f" | tokens {metric.tokens.total_tokens}"
            self.console.print(
                f"   • {metric.name}: {metric.duration_ms / 1000:.2f}s "
                f"[{metric.status}]{count_label}{token_label}"
            )
        for metric in recorder.domain_stages:
            domain = metric.attributes.get("domain", "unknown")
            self.console.print(
                f"   • {domain}/{metric.name}: "
                f"{metric.duration_ms / 1000:.2f}s [{metric.status}]"
            )
        self.console.print(
            f"   • total: {(recorder.duration_ms or 0) / 1000:.2f}s "
            f"[{recorder.status}]"
        )

    def _save_performance_report(
        self,
        recorder: PerformanceRecorder,
        report: Dict[str, object],
    ) -> None:
        """Persist metrics when supported without affecting run success."""

        storage = getattr(self, "storage", None)
        save_report = getattr(storage, "save_performance_report", None)
        if not callable(save_report):
            return
        try:
            metrics_path = save_report(recorder.run_id, report)
        except Exception as exc:
            self.console.print(
                f"[yellow]⚠️  Failed to save performance report: "
                f"{type(exc).__name__}: {exc}[/yellow]"
            )
            return
        self.console.print(f"📈 Saved performance report to: {metrics_path}\n")

    def _determine_time_window(self, force_hours: int = None) -> datetime:
        if force_hours:
            since = datetime.now(timezone.utc) - timedelta(hours=force_hours)
        else:
            hours = self.config.filtering.time_window_hours
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
        return since

    def _publish_github_pages_summary(
        self,
        *,
        summary: str,
        date: str,
        language: str,
        domain: Optional[str] = None,
        domain_name: Optional[str] = None,
    ) -> Optional[Path]:
        """Write a Jekyll post when GitHub Pages publishing is enabled."""
        if not self.config.github_pages.enabled:
            return None

        domain_part = f"-{domain}" if domain else ""
        post_filename = f"{date}-summary{domain_part}-{language}.md"
        posts_dir = Path("docs/_posts")
        posts_dir.mkdir(parents=True, exist_ok=True)
        dest_path = safe_output_path(posts_dir, post_filename)

        title_prefix = f"Horizon {domain_name}" if domain_name else "Horizon"
        page_title = f"{title_prefix} Summary: {date} ({language.upper()})"
        domain_front_matter = (
            f"domain: {json.dumps(domain)}\n" if domain else ""
        )
        front_matter = (
            "---\n"
            "layout: default\n"
            f"title: {json.dumps(page_title, ensure_ascii=False)}\n"
            f"date: {date}\n"
            f"lang: {language}\n"
            f"{domain_front_matter}"
            "---\n\n"
        )

        summary_content = summary
        first_line = summary_content.strip().split("\n")[0]
        if first_line.startswith("# "):
            parts = summary_content.split("\n", 1)
            if len(parts) > 1:
                summary_content = parts[1].strip()

        dest_path.write_text(front_matter + summary_content, encoding="utf-8")
        return dest_path

    async def fetch_all_sources(self, since: datetime) -> List[ContentItem]:
        """Fetch content from all configured sources.

        This is a stable stage entry point for integrations such as MCP.

        Args:
            since: Fetch items published after this time

        Returns:
            List[ContentItem]: All fetched items
        """
        self.last_fetch_report = None
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []

            # GitHub sources
            if self.config.sources.github:
                github_scraper = GitHubScraper(self.config.sources.github, client)
                tasks.append(self._fetch_with_progress("GitHub", github_scraper, since))

            # Hacker News
            if self.config.sources.hackernews.enabled:
                hn_scraper = HackerNewsScraper(self.config.sources.hackernews, client)
                tasks.append(self._fetch_with_progress("Hacker News", hn_scraper, since))

            # RSS feeds
            if self.config.sources.rss:
                from .extractors import ExtractorRegistry
                rss_scraper = RSSScraper(
                    self.config.sources.rss,
                    client,
                    ExtractorRegistry(self.config.extractors),
                )
                tasks.append(self._fetch_with_progress("RSS Feeds", rss_scraper, since))

            # Reddit
            if self.config.sources.reddit.enabled:
                reddit_scraper = RedditScraper(self.config.sources.reddit, client)
                tasks.append(self._fetch_with_progress("Reddit", reddit_scraper, since))

            # Telegram
            if self.config.sources.telegram.enabled:
                telegram_scraper = TelegramScraper(self.config.sources.telegram, client)
                tasks.append(self._fetch_with_progress("Telegram", telegram_scraper, since))

            # Twitter (Apify or Playwright mode)
            if self.config.sources.twitter and self.config.sources.twitter.enabled:
                tw_cfg = self.config.sources.twitter
                if tw_cfg.mode == "playwright":
                    twitter_scraper = TwitterPlaywrightScraper(tw_cfg)
                else:
                    twitter_scraper = TwitterScraper(tw_cfg, client)
                tasks.append(self._fetch_with_progress("Twitter", twitter_scraper, since))

            # OpenBB (financial news / filings via the OpenBB Platform SDK)
            if self.config.sources.openbb and self.config.sources.openbb.enabled:
                openbb_scraper = OpenBBScraper(self.config.sources.openbb, client)
                tasks.append(self._fetch_with_progress("OpenBB", openbb_scraper, since))

            # Google News RSS (key-less news search)
            if self.config.sources.google_news and self.config.sources.google_news.enabled:
                gn_scraper = GoogleNewsScraper(self.config.sources.google_news, client)
                tasks.append(self._fetch_with_progress("Google News", gn_scraper, since))

            # Fetch all concurrently
            outcomes = await asyncio.gather(*tasks)
            self.last_fetch_report = FetchReport(outcomes=list(outcomes))

            # Flatten successful and empty outcomes; failures remain in the report.
            all_items: List[ContentItem] = []
            for outcome in outcomes:
                all_items.extend(outcome.items)

            return all_items

    async def _fetch_with_progress(
        self, name: str, scraper, since: datetime
    ) -> SourceFetchOutcome:
        """Fetch from a scraper with progress indication.

        Args:
            name: Source name for display
            scraper: Scraper instance
            since: Fetch items after this time

        Returns:
            SourceFetchOutcome: Named fetch result and diagnostics
        """
        recorder = getattr(self, "_performance_recorder", None)
        measurement_context = (
            recorder.source_fetch(name) if recorder is not None else nullcontext()
        )
        with measurement_context as measurement:
            self.console.print(f"🔍 Fetching from {name}...")
            try:
                items = await scraper.fetch(since)
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                if measurement is not None:
                    measurement.mark_failure(exc)
                    measurement.set_result(output_items=0)
                self.console.print(f"[red]   Failed to fetch {name}: {error}[/red]")
                return SourceFetchOutcome(
                    source_name=name,
                    status="failure",
                    error=error,
                )

            status = "success" if items else "empty"
            if measurement is not None:
                measurement.set_result(status=status, output_items=len(items))
            self.console.print(f"   Found {len(items)} items from {name}")

            # Show per-sub-source breakdown when there are multiple sub-sources
            sub_counts: Dict[str, int] = defaultdict(int)
            for item in items:
                sub_counts[self._sub_source_label(item)] += 1
            if len(sub_counts) > 1:
                for sub, count in sorted(sub_counts.items()):
                    self.console.print(f"      • {sub}: {count}")

            return SourceFetchOutcome(
                source_name=name,
                status=status,
                items=items,
            )

    @staticmethod
    def _sub_source_label(item: ContentItem) -> str:
        """Return a human-readable sub-source label for an item."""
        meta = item.metadata
        if meta.get("subreddit"):
            return f"r/{meta['subreddit']}"
        if meta.get("feed_name"):
            return meta["feed_name"]
        if meta.get("channel"):
            return f"@{meta['channel']}"
        if meta.get("repo"):
            return meta["repo"]
        if meta.get("watchlist"):
            return meta["watchlist"]
        if meta.get("source_name"):
            return meta["source_name"]
        if meta.get("gn_query"):
            return f"google_news:{meta['gn_query']}"
        if meta.get("domain"):
            return meta["domain"]
        return item.author or "unknown"

    def merge_cross_source_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge items that point to the same URL from different sources.

        This is a stable stage helper for integrations such as MCP.

        Keeps the item with the richest content and combines metadata.

        Args:
            items: Items to deduplicate

        Returns:
            List[ContentItem]: Deduplicated items
        """
        # Group by normalized URL
        url_groups: Dict[tuple[str, str, str, str, Optional[int], str, str], List[ContentItem]] = {}
        for item in items:
            key = _deduplication_url_key(str(item.url))
            url_groups.setdefault(key, []).append(item)

        merged = []
        for group in url_groups.values():
            group_copies = [item.model_copy(deep=True) for item in group]
            if len(group) == 1:
                merged.append(group_copies[0])
                continue

            # Pick the item with the richest content as primary
            primary = max(group_copies, key=lambda x: len(x.content or ""))

            # Merge metadata and source info from other items
            all_sources = []
            for item in group_copies:
                if item.source_type.value not in all_sources:
                    all_sources.append(item.source_type.value)
                # Merge metadata (engagement, discussion, etc.)
                for mk, mv in item.metadata.items():
                    if mk not in primary.metadata or not primary.metadata[mk]:
                        primary.metadata[mk] = mv

                # Append content (e.g., comments from another source)
                if item is not primary and item.content:
                    if primary.content and item.content not in primary.content:
                        primary.content = (primary.content or "") + f"\n\n--- From {item.source_type.value} ---\n" + item.content

            primary.metadata["merged_sources"] = all_sources
            merged.append(primary)

        return merged

    async def merge_topic_duplicates(
        self,
        items: List[ContentItem],
        *,
        log: bool = True,
        ai_semaphore: Optional[asyncio.Semaphore] = None,
    ) -> List[ContentItem]:
        """Merge items covering the same topic using AI semantic deduplication.

        This is a stable stage helper for integrations such as MCP.

        Sends all item titles, tags, and summaries to AI in a single call.
        Items must already be sorted by ai_score descending so that the first
        item in each duplicate group is always the highest-scored one.
        Content (comments) from duplicate items is merged into the primary.

        Falls back to returning items unchanged if the AI call fails.
        """
        if len(items) <= 1:
            return items

        from .ai.prompts import TOPIC_DEDUP_SYSTEM, TOPIC_DEDUP_USER
        from .ai.utils import parse_json_response

        # Build the item list for the prompt
        lines = []
        for i, item in enumerate(items):
            tags = ", ".join(item.ai_tags) if item.ai_tags else "—"
            summary = item.ai_summary or "—"
            lines.append(f"[{i}] {item.title}\n    Tags: {tags}\n    Summary: {summary}")
        items_text = "\n\n".join(lines)

        try:
            ai_client = create_ai_client(
                self.config.ai.for_stage(AIStage.DEDUPLICATION)
            )
            if ai_semaphore is None:
                response = await ai_client.complete(
                    system=TOPIC_DEDUP_SYSTEM,
                    user=TOPIC_DEDUP_USER.format(items=items_text),
                )
            else:
                async with ai_semaphore:
                    response = await ai_client.complete(
                        system=TOPIC_DEDUP_SYSTEM,
                        user=TOPIC_DEDUP_USER.format(items=items_text),
                    )
            result = parse_json_response(response)
            if result is None:
                if log:
                    self.console.print("[yellow]  dedup: could not parse AI response, skipping[/yellow]")
                return items

            duplicate_groups = result.get("duplicates", [])
        except Exception as e:
            if log:
                self.console.print(f"[yellow]  dedup: AI call failed ({e}), skipping[/yellow]")
            return items

        if not duplicate_groups:
            return items

        # Build a set of indices to drop (all non-primary duplicates)
        drop_indices: set[int] = set()
        for group in duplicate_groups:
            if not isinstance(group, list) or len(group) < 2:
                continue
            primary_idx = group[0]
            if primary_idx < 0 or primary_idx >= len(items):
                continue
            primary = items[primary_idx]
            for dup_idx in group[1:]:
                if not isinstance(dup_idx, int) or dup_idx < 0 or dup_idx >= len(items):
                    continue
                if dup_idx == primary_idx:
                    continue
                dup = items[dup_idx]
                # Merge comments/content from the duplicate into the primary
                if dup.content:
                    if not primary.content or dup.content not in primary.content:
                        label = dup.source_type.value
                        primary.content = (primary.content or "") + f"\n\n--- From {label} ---\n{dup.content}"
                if log:
                    self.console.print(
                        f"   [dim]dedup: keep [{primary_idx}] {primary.title}[/dim]\n"
                        f"   [dim]       drop [{dup_idx}] {dup.title}[/dim]"
                    )
                drop_indices.add(dup_idx)

        return [item for i, item in enumerate(items) if i not in drop_indices]

    async def filter_items(
        self,
        items: List[ContentItem],
        *,
        threshold: Optional[float] = None,
        topic_dedup: bool = True,
        apply_balance: bool = True,
        log: bool = True,
        ai_semaphore: Optional[asyncio.Semaphore] = None,
    ) -> FilteringPipelineResult:
        """Apply score thresholding, optional topic dedup, and digest balancing."""
        effective_threshold = (
            threshold
            if threshold is not None
            else self.config.filtering.ai_score_threshold
        )
        threshold_items = [
            item
            for item in items
            if item.ai_score is not None and item.ai_score >= effective_threshold
        ]
        threshold_items.sort(key=lambda item: item.ai_score or 0, reverse=True)

        if log:
            self.console.print(
                f"⭐️ {len(threshold_items)} items scored ≥ {effective_threshold}\n"
            )

        deduped_items = threshold_items
        if topic_dedup and deduped_items:
            if ai_semaphore is None:
                deduped_items = await self.merge_topic_duplicates(
                    deduped_items,
                    log=log,
                )
            else:
                deduped_items = await self.merge_topic_duplicates(
                    deduped_items,
                    log=log,
                    ai_semaphore=ai_semaphore,
                )
        topic_dedup_removed = len(threshold_items) - len(deduped_items)

        if log and topic_dedup_removed:
            self.console.print(
                f"🧹 Removed {topic_dedup_removed} topic duplicates "
                f"→ {len(deduped_items)} unique items\n"
            )

        balanced_digest = (
            self.apply_balanced_digest(deduped_items, log=log)
            if apply_balance
            else BalancedDigestResult(items=deduped_items)
        )
        return FilteringPipelineResult(
            items=balanced_digest.items,
            threshold_count=len(threshold_items),
            topic_dedup_count=len(deduped_items),
            topic_dedup_removed=topic_dedup_removed,
            balanced_digest=balanced_digest,
        )

    def apply_balanced_digest(
        self,
        items: List[ContentItem],
        *,
        filtering: Optional[FilteringConfig] = None,
        log: bool = True,
    ) -> BalancedDigestResult:
        """Apply configured category quotas and the final item cap.

        Categories are read from ``item.metadata["category"]``. If a category
        appears in more than one configured group, the first group in config
        order wins.
        """
        filtering = filtering or self.config.filtering
        groups = filtering.category_groups
        max_items = filtering.max_items

        if not groups and max_items is None:
            return BalancedDigestResult(items=items)

        sorted_items = sorted(
            items,
            key=lambda item: item.ai_score or 0,
            reverse=True,
        )

        category_to_group: Dict[str, str] = {}
        duplicate_categories: List[str] = []
        for group_key, group in groups.items():
            for category in group.categories:
                if category in category_to_group:
                    if category_to_group[category] != group_key:
                        duplicate_categories.append(category)
                    continue
                category_to_group[category] = group_key

        if log:
            for category in sorted(set(duplicate_categories)):
                first_group = category_to_group[category]
                self.console.print(
                    f"[yellow]Warning: category '{category}' is configured in multiple "
                    f"groups; using '{first_group}'.[/yellow]"
                )

        selected: List[tuple[ContentItem, str]] = []
        group_counts: Dict[str, int] = defaultdict(int)
        default_group = filtering.default_group

        for item in sorted_items:
            category = item.metadata.get("category")
            group_key = (
                category_to_group.get(category, default_group)
                if isinstance(category, str)
                else default_group
            )

            if group_key in groups:
                limit = groups[group_key].limit
            else:
                limit = filtering.default_group_limit

            if limit is not None and group_counts[group_key] >= limit:
                continue

            selected.append((item, group_key))
            group_counts[group_key] += 1

        if max_items is not None:
            selected = selected[:max_items]

        final_counts: Dict[str, int] = defaultdict(int)
        for _, group_key in selected:
            final_counts[group_key] += 1

        group_limits: Dict[str, Optional[int]] = {
            group_key: group.limit for group_key, group in groups.items()
        }
        group_limits.setdefault(default_group, filtering.default_group_limit)

        if log:
            self.console.print(
                f"⚖️ Balanced digest selected {len(selected)}/{len(items)} items"
            )
            for group_key, group in groups.items():
                label = group.name or group_key
                self.console.print(
                    f"      • {label}: {final_counts.get(group_key, 0)}/{group.limit}"
                )
            if (
                final_counts.get(default_group, 0)
                or filtering.default_group_limit is not None
            ):
                limit_label = (
                    str(filtering.default_group_limit)
                    if filtering.default_group_limit is not None
                    else "unlimited"
                )
                self.console.print(
                    f"      • {default_group}: "
                    f"{final_counts.get(default_group, 0)}/{limit_label}"
                )
            self.console.print("")

        return BalancedDigestResult(
            items=[item for item, _ in selected],
            enabled=True,
            group_counts=dict(final_counts),
            group_limits=group_limits,
            duplicate_categories=sorted(set(duplicate_categories)),
        )

    async def _expand_twitter_discussion(
        self,
        items: List[ContentItem],
        domain_key: Optional[str] = None,
        domain_config: Optional[DomainConfig] = None,
    ) -> None:
        """Second-stage: fetch reply text for important Twitter items and re-analyze.

        Only runs when sources.twitter.fetch_reply_text is True.
        Bounded by max_tweets_to_expand to control cost.
        """
        tw_cfg = self.config.sources.twitter
        if not tw_cfg or not tw_cfg.enabled or not tw_cfg.fetch_reply_text:
            return

        from .models import SourceType

        twitter_items = [
            item for item in items
            if item.source_type == SourceType.TWITTER
        ][:tw_cfg.max_tweets_to_expand]

        if not twitter_items:
            return

        self.console.print(
            f"💬 Fetching reply text for {len(twitter_items)} Twitter items..."
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            if tw_cfg.mode == "playwright":
                self.console.print(
                    "   [yellow]Reply expansion not yet supported in Playwright mode.[/yellow]"
                )
                return
            scraper = TwitterScraper(tw_cfg, client)
            expanded = []
            for item in twitter_items:
                try:
                    reply_lines = await scraper.fetch_replies_for_item(item)
                    if TwitterScraper.append_discussion_content(item, reply_lines):
                        expanded.append(item)
                        self.console.print(
                            f"   💬 {len(reply_lines)} replies added to: {item.title[:60]}"
                        )
                except Exception as exc:
                    self.console.print(
                        f"   [yellow]⚠️  Reply fetch failed for {item.id}: {exc}[/yellow]"
                    )

        if not expanded:
            return

        self.console.print(
            f"   Re-analyzing {len(expanded)} Twitter items with reply context...\n"
        )
        ai_client = create_ai_client(self.config.ai.for_stage(AIStage.ANALYSIS))
        if domain_key is None:
            analyzer = ContentAnalyzer(ai_client)
        else:
            analyzer = ContentAnalyzer(
                ai_client,
                semaphore=self._domain_ai_semaphore,
                domain_guidance=(
                    domain_config.analysis_guidance if domain_config else None
                ),
                show_progress=False,
            )
        await analyzer.analyze_batch(expanded)

    async def _enrich_important_items(
        self,
        items: List[ContentItem],
        domain_key: Optional[str] = None,
        domain_config: Optional[DomainConfig] = None,
    ) -> None:
        """Enrich items with background knowledge (2nd AI pass).

        For each item that passed the score threshold, call AI to generate
        background knowledge based on the item's actual content.

        Args:
            items: Important items to enrich (modified in-place)
        """
        if not items:
            return

        self.console.print("📚 Enriching with background knowledge...")
        ai_client = create_ai_client(self.config.ai.for_stage(AIStage.ENRICHMENT))
        translation_client = create_ai_client(
            self.config.ai.for_stage(AIStage.TRANSLATION)
        )
        if domain_key is None:
            enricher = ContentEnricher(
                ai_client,
                translation_client=translation_client,
            )
        else:
            enricher = ContentEnricher(
                ai_client,
                translation_client=translation_client,
                semaphore=self._domain_ai_semaphore,
                search_semaphore=self._domain_search_semaphore,
                domain_guidance=(
                    domain_config.enrichment_guidance
                    if domain_config
                    else None
                ),
                show_progress=False,
            )
        await enricher.enrich_batch(items)
        self.console.print(f"   Enriched {len(items)} items\n")

    async def _analyze_content(
        self,
        items: List[ContentItem],
        domain_key: Optional[str] = None,
        domain_config: Optional[DomainConfig] = None,
    ) -> List[ContentItem]:
        """Analyze content items with AI.

        Args:
            items: Items to analyze

        Returns:
            List[ContentItem]: Analyzed items
        """
        self.console.print("🤖 Analyzing content with AI...")

        ai_client = create_ai_client(self.config.ai.for_stage(AIStage.ANALYSIS))
        if domain_key is None:
            analyzer = ContentAnalyzer(ai_client)
        else:
            analyzer = ContentAnalyzer(
                ai_client,
                semaphore=self._domain_ai_semaphore,
                domain_guidance=(
                    domain_config.analysis_guidance if domain_config else None
                ),
                show_progress=False,
            )

        return await analyzer.analyze_batch(items)
