from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ── Default fallback plan (used when LLM is unavailable) ─────────────
_FALLBACK_STEPS: List[Dict[str, Any]] = [
    {
        "id": "ingest",
        "description": "Ingest and profile uploaded data",
        "type": "data_prep",
        "required_node": "data_ingest",
        "status": "pending",
        "depends_on": [],
        "result_ref": None,
    },
    {
        "id": "analyze",
        "description": "Generate and execute analysis code",
        "type": "analysis",
        "required_node": "executor",
        "status": "pending",
        "depends_on": ["ingest"],
        "result_ref": None,
    },
    {
        "id": "respond",
        "description": "Summarize findings and next steps",
        "type": "visualization",
        "required_node": "responder",
        "status": "pending",
        "depends_on": ["analyze"],
        "result_ref": None,
    },
]


def init_plan(goal: str, steps: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Create an initial plan from the given steps (or fall back to defaults)."""
    if steps is None:
        steps = [dict(s) for s in _FALLBACK_STEPS]  # deep-copy defaults
    else:
        # Normalize LLM-generated steps: ensure required fields exist
        for i, step in enumerate(steps):
            step.setdefault("id", f"step_{i+1}")
            step.setdefault("status", "pending")
            step.setdefault("depends_on", [])
            step.setdefault("result_ref", None)
            step.setdefault("type", "analysis")
            # Map step type to required node
            stype = step.get("type", "analysis")
            if "required_node" not in step:
                step["required_node"] = _type_to_node(stype)

    return {
        "plan_version": 1,
        "plan_steps": steps,
        "current_step_id": None,
        "plan_status": "approved",
        "goal": goal,
    }


def _type_to_node(step_type: str) -> str:
    """Map a step type to the graph node that should execute it."""
    mapping = {
        "data_prep": "data_ingest",
        "analysis": "executor",
        "visualization": "executor",
        "qc": "qc",
    }
    return mapping.get(step_type, "executor")


def select_next_step(plan_steps: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Return the first pending or in-progress step."""
    for step in plan_steps:
        if step.get("status") in {"pending", "in_progress"}:
            return step
    return None


def mark_step(
    plan_steps: List[Dict[str, Any]],
    step_id: str,
    status: str,
    result_ref: Any = None,
):
    """Update the status of a specific step."""
    for step in plan_steps:
        if step.get("id") == step_id:
            step["status"] = status
            if result_ref is not None:
                step["result_ref"] = result_ref
            break


def parse_plan_json(raw: str) -> Optional[List[Dict[str, Any]]]:
    """Try to parse a JSON plan from LLM output.

    The LLM might wrap the JSON in a markdown code fence, so we try to
    extract it first.  Returns None on failure.
    """
    text = raw.strip()

    # Strip markdown fences if present
    if text.startswith("```"):
        lines = text.splitlines()
        # Remove first and last fence lines
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip().startswith("```"):
                end = i
                break
        text = "\n".join(lines[start:end]).strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "steps" in data:
            return data["steps"]
        logger.warning("LLM plan JSON is not a list or dict with 'steps' key")
        return None
    except json.JSONDecodeError as e:
        logger.warning("Failed to parse LLM plan JSON: %s", e)
        return None
