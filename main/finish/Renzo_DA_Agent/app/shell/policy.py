from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from renzo.app.shell.schema import ShellDecision


SHELL_PERSONA = "concise_stable_professional"
MAX_SHELL_LINES = 6


_MUTATION_TOOLS = {
    "create_workflow",
    "start_experiment_from_workflow",
    "run_engine_turn",
    "engine_control",
    "link_experiment",
}


@dataclass
class PendingAction:
    action_id: str
    action_type: str
    title: str
    summary: str
    steps: List[str]
    requires_confirm: bool
    payload: Dict

    def to_dict(self) -> Dict:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "title": self.title,
            "summary": self.summary,
            "steps": list(self.steps),
            "requires_confirm": self.requires_confirm,
            "payload": self.payload,
        }


def is_mutation_tool(name: str) -> bool:
    return (name or "").strip() in _MUTATION_TOOLS


def decision_requires_confirm(decision: ShellDecision) -> bool:
    if decision.confirm_required:
        return True
    for call in decision.tool_calls:
        if is_mutation_tool(call.name):
            return True
    return False


def enforce_confirmation_policy(decision: ShellDecision) -> ShellDecision:
    decision.confirm_required = decision_requires_confirm(decision)
    return decision


def control_command_requires_confirm(command: str) -> bool:
    # No confirmation for control commands: clicking Continue (or Pause/Stop/etc.) is equivalent to typing it.
    return False
