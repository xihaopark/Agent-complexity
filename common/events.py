from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RunEvent(BaseModel):
    timestamp: datetime = Field(default_factory=utc_now)
    job_id: str
    run_id: str
    phase: str
    event_type: str
    actor: str | None = None
    target: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    trace_id: str | None = None


class MetricRecord(BaseModel):
    metric_code: str
    scope: Literal["system", "task", "run"] = "system"
    run_id: str | None = None
    raw_value: float | None = None
    value_json: dict[str, Any] = Field(default_factory=dict)
    agg_type: str = "raw"
    ci_low: float | None = None
    ci_high: float | None = None
    evidence_ref: str | None = None


class ArtifactRef(BaseModel):
    artifact_type: str
    uri: str
    sha256: str | None = None
    size: int | None = None
    created_at: datetime = Field(default_factory=utc_now)
