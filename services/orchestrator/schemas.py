from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class RunSpecModel(BaseModel):
    setup_commands: list[str] = Field(default_factory=list)
    entry_command: str | None = None
    task_inputs: list[dict[str, Any]] = Field(default_factory=list)
    env_allowlist: list[str] = Field(default_factory=list)
    repeats: int | None = None
    timeout_sec: int | None = None


class AnalysisCreateRequest(BaseModel):
    repo_url: HttpUrl
    git_ref: str = "main"
    auth_ref: str | None = None
    auth_token: str | None = Field(default=None, repr=False)
    run_profile: str = "standard"
    run_spec: RunSpecModel | None = None
    repeats: int | None = None
    timeout_sec: int | None = None


class AnalysisCreateResponse(BaseModel):
    analysis_id: str
    status_url: str


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    status: str
    repo_url: str
    git_ref: str
    run_profile: str
    repeats: int
    timeout_sec: int
    error_summary: str | None
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None
    finished_at: datetime | None


class ReportInfoResponse(BaseModel):
    analysis_id: str
    status: str
    report_markdown_uri: str | None
    report_html_uri: str | None
    metadata: dict[str, Any] = Field(default_factory=dict)


class MetricResponse(BaseModel):
    metric_code: str
    scope: str
    run_id: str | None
    raw_value: float | None
    value_json: dict[str, Any]
    agg_type: str
    ci_low: float | None
    ci_high: float | None
    evidence_ref: str | None


class ArtifactResponse(BaseModel):
    artifact_type: str
    uri: str
    sha256: str | None
    size_bytes: int | None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
