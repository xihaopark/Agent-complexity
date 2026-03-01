from __future__ import annotations

from typing import Any

from common.settings import get_settings
from services.orchestrator.constants import AnalysisStatus
from services.orchestrator.db import session_scope
from services.orchestrator.repository import AnalysisRepository
from services.orchestrator.schemas import AnalysisCreateRequest
from services.orchestrator.secrets import get_secret_store


def normalize_request(request: AnalysisCreateRequest) -> AnalysisCreateRequest:
    settings = get_settings()
    payload = request.model_copy(deep=True)
    if payload.repeats is None:
        payload.repeats = settings.default_repeats
    payload.repeats = max(1, min(payload.repeats, settings.max_repeats))
    if payload.timeout_sec is None:
        payload.timeout_sec = settings.default_timeout_sec
    if payload.run_spec:
        if payload.run_spec.repeats is None:
            payload.run_spec.repeats = payload.repeats
        if payload.run_spec.timeout_sec is None:
            payload.run_spec.timeout_sec = payload.timeout_sec
    return payload


def enqueue_analysis(request: AnalysisCreateRequest) -> dict[str, Any]:
    payload = normalize_request(request)
    secret_store = get_secret_store()
    auth_ref = payload.auth_ref
    if payload.auth_token:
        auth_ref = secret_store.put_token(payload.auth_token)

    with session_scope() as session:
        repo = AnalysisRepository(session)
        job = repo.create_job(payload=payload, auth_ref=auth_ref)

    from workers.sandbox_runner.celery_app import celery_app

    celery_app.send_task("workers.sandbox_runner.tasks.run_analysis_pipeline", args=[job.id])
    return {"analysis_id": job.id, "status": AnalysisStatus.QUEUED.value}
