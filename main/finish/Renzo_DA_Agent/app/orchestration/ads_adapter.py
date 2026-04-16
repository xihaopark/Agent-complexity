from __future__ import annotations

from typing import Any, Dict, List


def make_stage_orchestrator(stages: List[Dict[str, Any]], criteria: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "high_level_stages": stages,
        "high_level_success_criteria": criteria,
    }
