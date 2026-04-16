from __future__ import annotations

from typing import Dict

from renzo.app.state import AgentState


def preprocess_node(state: AgentState) -> Dict:
    data_profile = state.get("data_profile", {})
    if not data_profile:
        return {"next_node": "planner"}

    return {
        "next_node": "planner",
    }
