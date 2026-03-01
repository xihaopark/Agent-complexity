from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import select

from common.logging import setup_logging
from common.settings import get_settings
from services.orchestrator.db import init_db, session_scope
from services.orchestrator.models import AnalysisArtifact, AnalysisMetric
from services.orchestrator.orchestrator import enqueue_analysis
from services.orchestrator.repository import AnalysisRepository
from services.orchestrator.schemas import (
    AnalysisCreateRequest,
    AnalysisCreateResponse,
    AnalysisStatusResponse,
    ArtifactResponse,
    MetricResponse,
    ReportInfoResponse,
)

setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(title="Agentic Complexity Analyzer API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _download_uri(uri: str) -> str:
    try:
        path = Path(uri)
        root = settings.artifact_root.resolve()
        if path.is_absolute() and (root in path.parents or path == root):
            relative = path.relative_to(root)
            return f"/api/v1/files?path={quote(str(relative))}"
    except Exception:
        pass
    return uri


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/analyses", response_model=AnalysisCreateResponse)
def create_analysis(request: AnalysisCreateRequest) -> AnalysisCreateResponse:
    result = enqueue_analysis(request)
    return AnalysisCreateResponse(
        analysis_id=result["analysis_id"],
        status_url=f"/api/v1/analyses/{result['analysis_id']}",
    )


@app.get("/api/v1/analyses/{analysis_id}", response_model=AnalysisStatusResponse)
def get_analysis_status(analysis_id: str) -> AnalysisStatusResponse:
    with session_scope() as session:
        repo = AnalysisRepository(session)
        job = repo.get_job(analysis_id)
        if job is None:
            raise HTTPException(status_code=404, detail="analysis not found")
        return AnalysisStatusResponse(
            analysis_id=job.id,
            status=job.status,
            repo_url=job.repo_url,
            git_ref=job.git_ref,
            run_profile=job.run_profile,
            repeats=job.repeats,
            timeout_sec=job.timeout_sec,
            error_summary=job.error_summary,
            created_at=job.created_at,
            updated_at=job.updated_at,
            started_at=job.started_at,
            finished_at=job.finished_at,
        )


@app.get("/api/v1/analyses/{analysis_id}/report", response_model=ReportInfoResponse)
def get_report(analysis_id: str) -> ReportInfoResponse:
    with session_scope() as session:
        repo = AnalysisRepository(session)
        job = repo.get_job(analysis_id)
        if job is None:
            raise HTTPException(status_code=404, detail="analysis not found")
        artifacts = session.scalars(
            select(AnalysisArtifact).where(AnalysisArtifact.analysis_id == analysis_id)
        ).all()
        md_artifact = next((a for a in artifacts if a.artifact_type == "report_markdown"), None)
        html_artifact = next((a for a in artifacts if a.artifact_type == "report_html"), None)
        return ReportInfoResponse(
            analysis_id=analysis_id,
            status=job.status,
            report_markdown_uri=_download_uri(md_artifact.uri) if md_artifact else None,
            report_html_uri=_download_uri(html_artifact.uri) if html_artifact else None,
            metadata={
                "observability_coverage": job.observability_coverage,
                "composite_score": job.composite_score,
            },
        )


@app.get("/api/v1/analyses/{analysis_id}/metrics", response_model=list[MetricResponse])
def list_metrics(analysis_id: str) -> list[MetricResponse]:
    with session_scope() as session:
        rows = session.scalars(
            select(AnalysisMetric).where(AnalysisMetric.analysis_id == analysis_id)
        ).all()
        return [
            MetricResponse(
                metric_code=row.metric_code,
                scope=row.scope,
                run_id=row.run_id,
                raw_value=row.raw_value,
                value_json=row.value_json or {},
                agg_type=row.agg_type,
                ci_low=row.ci_low,
                ci_high=row.ci_high,
                evidence_ref=row.evidence_ref,
            )
            for row in rows
        ]


@app.get("/api/v1/analyses/{analysis_id}/artifacts", response_model=list[ArtifactResponse])
def list_artifacts(analysis_id: str) -> list[ArtifactResponse]:
    with session_scope() as session:
        rows = session.scalars(
            select(AnalysisArtifact).where(AnalysisArtifact.analysis_id == analysis_id)
        ).all()
        return [
            ArtifactResponse(
                artifact_type=row.artifact_type,
                uri=_download_uri(row.uri),
                sha256=row.sha256,
                size_bytes=row.size_bytes,
                metadata_json=row.metadata_json or {},
            )
            for row in rows
        ]


@app.get("/api/v1/files")
def download_artifact(path: str) -> FileResponse:
    """
    Download files under AGENTIC_ARTIFACT_ROOT.
    """
    root = settings.artifact_root.resolve()
    target = (root / path).resolve()
    if root not in target.parents and target != root:
        raise HTTPException(status_code=400, detail="invalid artifact path")
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(target)


def run() -> None:
    import uvicorn

    uvicorn.run("apps.api.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
