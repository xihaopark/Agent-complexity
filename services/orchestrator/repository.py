from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from common.events import ArtifactRef, MetricRecord
from services.orchestrator.constants import AnalysisStatus
from services.orchestrator.models import AnalysisArtifact, AnalysisJob, AnalysisMetric
from services.orchestrator.schemas import AnalysisCreateRequest


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AnalysisRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_job(self, payload: AnalysisCreateRequest, auth_ref: str | None) -> AnalysisJob:
        run_spec_dict = payload.run_spec.model_dump() if payload.run_spec else {}
        job = AnalysisJob(
            repo_url=str(payload.repo_url),
            git_ref=payload.git_ref,
            auth_ref=auth_ref,
            run_profile=payload.run_profile,
            run_spec=run_spec_dict,
            repeats=payload.repeats,
            timeout_sec=payload.timeout_sec,
            status=AnalysisStatus.QUEUED.value,
        )
        self.session.add(job)
        self.session.flush()
        return job

    def get_job(self, analysis_id: str) -> AnalysisJob | None:
        return self.session.get(AnalysisJob, analysis_id)

    def update_job_status(
        self,
        job: AnalysisJob,
        status: AnalysisStatus,
        error_summary: str | None = None,
        observability_coverage: float | None = None,
    ) -> AnalysisJob:
        job.status = status.value
        if status == AnalysisStatus.RUNNING and not job.started_at:
            job.started_at = utcnow()
        if status in {AnalysisStatus.REPORT_READY, AnalysisStatus.FAILED, AnalysisStatus.PARTIAL}:
            job.finished_at = utcnow()
        if error_summary is not None:
            job.error_summary = error_summary
        if observability_coverage is not None:
            job.observability_coverage = observability_coverage
        self.session.add(job)
        return job

    def replace_metrics(self, analysis_id: str, metrics: Iterable[MetricRecord]) -> None:
        existing = self.session.scalars(
            select(AnalysisMetric).where(AnalysisMetric.analysis_id == analysis_id)
        ).all()
        for row in existing:
            self.session.delete(row)
        for metric in metrics:
            self.session.add(
                AnalysisMetric(
                    analysis_id=analysis_id,
                    metric_code=metric.metric_code,
                    scope=metric.scope,
                    run_id=metric.run_id,
                    raw_value=metric.raw_value,
                    value_json=metric.value_json,
                    agg_type=metric.agg_type,
                    ci_low=metric.ci_low,
                    ci_high=metric.ci_high,
                    evidence_ref=metric.evidence_ref,
                )
            )

    def replace_artifacts(self, analysis_id: str, artifacts: Iterable[ArtifactRef]) -> None:
        existing = self.session.scalars(
            select(AnalysisArtifact).where(AnalysisArtifact.analysis_id == analysis_id)
        ).all()
        for row in existing:
            self.session.delete(row)
        for artifact in artifacts:
            self.session.add(
                AnalysisArtifact(
                    analysis_id=analysis_id,
                    artifact_type=artifact.artifact_type,
                    uri=artifact.uri,
                    sha256=artifact.sha256,
                    size_bytes=artifact.size,
                    metadata_json={},
                )
            )
