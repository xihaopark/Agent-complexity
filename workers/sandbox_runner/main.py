from __future__ import annotations

import os

from workers.sandbox_runner.celery_app import celery_app


def run_worker() -> None:
    concurrency = int(os.getenv("AGENTIC_STANDARD_CONCURRENCY", "3"))
    celery_app.worker_main(
        [
            "worker",
            "--loglevel=INFO",
            f"--concurrency={concurrency}",
            "-Q",
            "celery",
        ]
    )


if __name__ == "__main__":
    run_worker()
