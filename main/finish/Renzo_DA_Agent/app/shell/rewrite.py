from __future__ import annotations

from typing import Dict, List


def _truncate_lines(text: str, max_lines: int = 6) -> str:
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    if not lines:
        return ""
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines - 1] + ["More details are available in Engine Detail."])


def rewrite_engine_summary_for_humans(
    engine_text: str,
    workflow_status: str = "",
    current_step_id: str = "",
) -> str:
    """Rewrite long engine output into a concise, user-friendly shell reply."""
    base = _truncate_lines(engine_text, max_lines=5)
    if not base:
        if workflow_status == "waiting_user":
            return "Current step is complete.\nKey outputs are ready.\nReply `continue` when you want the next step."
        if workflow_status == "failed":
            return "The latest step failed.\nI can help retry the step or adjust the plan."
        return "Update received.\nThe engine state is refreshed."

    prefix = ""
    if workflow_status == "waiting_user":
        prefix = "Step completed.\n"
    elif workflow_status == "running":
        prefix = "Engine updated.\n"
    elif workflow_status == "failed":
        prefix = "Step failed.\n"

    step_note = f"\nCurrent step: {current_step_id}" if current_step_id else ""
    return f"{prefix}{base}{step_note}".strip()


def build_shell_reply(
    content: str,
    *,
    chips: List[str] | None = None,
    pending_action: Dict | None = None,
    tone: str = "professional",
) -> Dict:
    return {
        "type": "shell_reply",
        "content": content,
        "tone": tone,
        "concise": True,
        "chips": chips or [],
        "pending_action": pending_action,
    }

