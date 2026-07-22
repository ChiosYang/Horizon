"""Structured performance measurements for a single Horizon run."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Dict, Optional
from uuid import uuid4

from .ai.tokens import TokenUsageSnapshot, get_usage_snapshot


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_utc(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


@dataclass
class TokenUsageDelta:
    """Token usage accumulated between two snapshots."""

    input_tokens: int = 0
    output_tokens: int = 0
    per_provider: Dict[str, Dict[str, int]] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "per_provider": self.per_provider,
        }


def token_usage_delta(
    before: TokenUsageSnapshot,
    after: TokenUsageSnapshot,
) -> TokenUsageDelta:
    """Return the non-negative token delta between two usage snapshots."""

    per_provider: Dict[str, Dict[str, int]] = {}
    provider_names = set(before.per_provider) | set(after.per_provider)
    for provider in sorted(provider_names):
        before_usage = before.per_provider.get(provider)
        after_usage = after.per_provider.get(provider)
        input_tokens = max(
            0,
            (after_usage.input_tokens if after_usage else 0)
            - (before_usage.input_tokens if before_usage else 0),
        )
        output_tokens = max(
            0,
            (after_usage.output_tokens if after_usage else 0)
            - (before_usage.output_tokens if before_usage else 0),
        )
        if input_tokens or output_tokens:
            per_provider[provider] = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            }

    return TokenUsageDelta(
        input_tokens=max(0, after.total_input_tokens - before.total_input_tokens),
        output_tokens=max(0, after.total_output_tokens - before.total_output_tokens),
        per_provider=per_provider,
    )


@dataclass
class PerformanceMetric:
    """One completed pipeline or source-fetch measurement."""

    name: str
    started_at: str
    completed_at: str
    duration_ms: float
    status: str
    input_items: Optional[int] = None
    output_items: Optional[int] = None
    error_type: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    tokens: TokenUsageDelta = field(default_factory=TokenUsageDelta)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["tokens"] = self.tokens.to_dict()
        return payload


class PerformanceMeasurement:
    """Context manager used to measure one operation with a monotonic clock."""

    def __init__(
        self,
        recorder: "PerformanceRecorder",
        name: str,
        *,
        destination: str,
        input_items: Optional[int] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.recorder = recorder
        self.name = name
        self.destination = destination
        self.input_items = input_items
        self.output_items: Optional[int] = None
        self.attributes = dict(attributes or {})
        self.status = "success"
        self.error_type: Optional[str] = None
        self._started_at: Optional[datetime] = None
        self._started_monotonic: Optional[float] = None
        self._usage_before: Optional[TokenUsageSnapshot] = None

    def __enter__(self) -> "PerformanceMeasurement":
        self._started_at = _utc_now()
        self._started_monotonic = perf_counter()
        self._usage_before = get_usage_snapshot()
        return self

    def set_result(
        self,
        *,
        status: Optional[str] = None,
        output_items: Optional[int] = None,
        **attributes: Any,
    ) -> None:
        """Attach result metadata before the measurement is completed."""

        if status is not None:
            self.status = status
        if output_items is not None:
            self.output_items = output_items
        self.attributes.update(attributes)

    def mark_failure(self, error: BaseException) -> None:
        """Record a handled exception without re-raising it from the stage."""

        self.status = "failure"
        self.error_type = type(error).__name__

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if self._started_at is None or self._started_monotonic is None:
            raise RuntimeError("Performance measurement was not started")

        if exc is not None:
            self.mark_failure(exc)

        completed_at = _utc_now()
        usage_after = get_usage_snapshot()
        metric = PerformanceMetric(
            name=self.name,
            started_at=_format_utc(self._started_at),
            completed_at=_format_utc(completed_at),
            duration_ms=round(
                max(0.0, perf_counter() - self._started_monotonic) * 1000,
                2,
            ),
            status=self.status,
            input_items=self.input_items,
            output_items=self.output_items,
            error_type=self.error_type,
            attributes=self.attributes,
            tokens=token_usage_delta(self._usage_before, usage_after),
        )
        self.recorder._record(metric, destination=self.destination)
        return False


class PerformanceRecorder:
    """Collect structured performance data for one Horizon run."""

    schema_version = 1

    def __init__(self, run_id: Optional[str] = None) -> None:
        started_at = _utc_now()
        self.run_id = run_id or (
            f"{started_at.strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
        )
        self.started_at = started_at
        self._started_monotonic = perf_counter()
        self._usage_before = get_usage_snapshot()
        self.completed_at: Optional[datetime] = None
        self.duration_ms: Optional[float] = None
        self.status = "running"
        self.error_type: Optional[str] = None
        self.stages: list[PerformanceMetric] = []
        self.source_fetches: list[PerformanceMetric] = []
        self.tokens = TokenUsageDelta()

    def stage(
        self,
        name: str,
        *,
        input_items: Optional[int] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> PerformanceMeasurement:
        return PerformanceMeasurement(
            self,
            name,
            destination="stages",
            input_items=input_items,
            attributes=attributes,
        )

    def source_fetch(self, source_name: str) -> PerformanceMeasurement:
        return PerformanceMeasurement(
            self,
            "fetch_source",
            destination="source_fetches",
            attributes={"source": source_name},
        )

    def _record(self, metric: PerformanceMetric, *, destination: str) -> None:
        if destination == "source_fetches":
            self.source_fetches.append(metric)
        else:
            self.stages.append(metric)

    def finish(self, status: str, *, error_type: Optional[str] = None) -> None:
        """Finalize the report. Repeated calls leave the first result intact."""

        if self.completed_at is not None:
            return
        self.completed_at = _utc_now()
        self.duration_ms = round(
            max(0.0, perf_counter() - self._started_monotonic) * 1000,
            2,
        )
        self.status = status
        self.error_type = error_type
        self.tokens = token_usage_delta(self._usage_before, get_usage_snapshot())

    def to_dict(self) -> Dict[str, Any]:
        if self.completed_at is None or self.duration_ms is None:
            raise RuntimeError("Performance report must be finished before serialization")
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "started_at": _format_utc(self.started_at),
            "completed_at": _format_utc(self.completed_at),
            "duration_ms": self.duration_ms,
            "status": self.status,
            "error_type": self.error_type,
            "tokens": self.tokens.to_dict(),
            "stages": [metric.to_dict() for metric in self.stages],
            "source_fetches": [
                metric.to_dict() for metric in self.source_fetches
            ],
        }
