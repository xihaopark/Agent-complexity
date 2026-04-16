from __future__ import annotations

import logging
from typing import Dict

from renzo.app.state import AgentState

logger = logging.getLogger(__name__)


def router_node(state: AgentState) -> Dict:
    next_node = state.get("next_node") or "planner"
    logger.info("[Router] -> %s (step=%s)", next_node, state.get("current_step_id", "-"))
    return {"next_node": next_node}
