from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.orchestrator.constants import AnalysisStatus
from services.orchestrator.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    repo_url: Mapped[str] = mapped_column(Text, nullable=False)
    git_ref: Mapped[str] = mapped_column(String(255), nullable=False, default="main")
    auth_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    run_profile: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    run_spec: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    repeats: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    timeout_sec: Mapped[int] = mapped_column(Integer, nullable=False, default=1800)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default=AnalysisStatus.QUEUED.value)
    error_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    artifact_root: Mapped[str | None] = mapped_column(Text, nullable=True)
    observability_coverage: Mapped[float | None] = mapped_column(Float, nullable=True)
    composite_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    metrics: Mapped[list["AnalysisMetric"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    artifacts: Mapped[list["AnalysisArtifact"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )


class AnalysisMetric(Base):
    __tablename__ = "analysis_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False
    )
    metric_code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    scope: Mapped[str] = mapped_column(String(16), nullable=False, default="system")
    run_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    agg_type: Mapped[str] = mapped_column(String(32), nullable=False, default="raw")
    ci_low: Mapped[float | None] = mapped_column(Float, nullable=True)
    ci_high: Mapped[float | None] = mapped_column(Float, nullable=True)
    evidence_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    job: Mapped[AnalysisJob] = relationship(back_populates="metrics")


class AnalysisArtifact(Base):
    __tablename__ = "analysis_artifacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False
    )
    artifact_type: Mapped[str] = mapped_column(String(64), nullable=False)
    uri: Mapped[str] = mapped_column(Text, nullable=False)
    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    job: Mapped[AnalysisJob] = relationship(back_populates="artifacts")
