from __future__ import annotations

import logging

from common.logging import setup_logging
from services.orchestrator.constants import AnalysisStatus
from services.orchestrator.db import session_scope
from services.orchestrator.repository import AnalysisRepository
from workers.sandbox_runner.celery_app import celery_app
from workers.sandbox_runner.pipeline import execute_analysis_pipeline

setup_logging()
logger = logging.getLogger(__name__)


@celery_app.task(name="workers.sandbox_runner.tasks.run_analysis_pipeline", bind=True)
def run_analysis_pipeline(self, analysis_id: str) -> dict[str, str]:
    logger.info("starting analysis pipeline for %s", analysis_id)
    try:
        execute_analysis_pipeline(analysis_id)
        return {"analysis_id": analysis_id, "status": "done"}
    except Exception as exc:  # pragma: no cover
        logger.exception("analysis pipeline failed for %s", analysis_id)
        with session_scope() as session:
            repo = AnalysisRepository(session)
            job = repo.get_job(analysis_id)
            if job:
                repo.update_job_status(job, AnalysisStatus.FAILED, error_summary=str(exc))
        raise
