from __future__ import annotations

from enum import StrEnum


class AnalysisStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    STATIC_DONE = "static_done"
    DYNAMIC_DONE = "dynamic_done"
    REPORT_READY = "report_ready"
    FAILED = "failed"
    PARTIAL = "partial"


TERMINAL_STATUSES = {AnalysisStatus.REPORT_READY, AnalysisStatus.FAILED, AnalysisStatus.PARTIAL}
