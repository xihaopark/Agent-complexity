from __future__ import annotations

from celery import Celery

from common.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "agentic_complexity",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["workers.sandbox_runner.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    task_track_started=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)
