"""hitl node — Human-in-the-Loop interaction point.

When any node (planner, coder, qc) encounters a decision that requires
human input, it sets hitl_pending=True along with the question/context
and routes here.

This node:
  1. Reads the HITL request fields from state.
  2. Signals to the WebSocket handler that a human response is needed
     (via a shared asyncio.Event registry).
  3. Waits for the human response to be written into state.
  4. Clears the HITL fields and routes back to the originating node.

The actual pause/resume is coordinated between this node and the
WebSocket handler in api_gateway.py via a shared event registry.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Dict

from langchain_core.messages import AIMessage

from renzo.app.state import AgentState

logger = logging.getLogger(__name__)

# ── Shared HITL Event Registry ────────────────────────────────────────
# Maps session_id -> asyncio.Event that is set when human responds.
# The WebSocket handler sets the event after writing hitl_response to state.
_hitl_events: Dict[str, asyncio.Event] = {}
_hitl_responses: Dict[str, str] = {}


def register_hitl_event(session_id: str) -> asyncio.Event:
    """Create and register an asyncio.Event for a session's HITL wait."""
    event = asyncio.Event()
    _hitl_events[session_id] = event
    return event


def resolve_hitl(session_id: str, response: str) -> None:
    """Called by the WebSocket handler when the human responds."""
    _hitl_responses[session_id] = response
    event = _hitl_events.get(session_id)
    if event:
        event.set()
    else:
        logger.warning("No HITL event found for session %s", session_id)


def get_hitl_response(session_id: str) -> str:
    """Retrieve and clear the stored HITL response."""
    return _hitl_responses.pop(session_id, "")


def clear_hitl_event(session_id: str) -> None:
    """Clean up HITL event after use."""
    _hitl_events.pop(session_id, None)
    _hitl_responses.pop(session_id, None)


def hitl_node(state: AgentState) -> Dict:
    """HITL node — processes a human-in-the-loop interaction.

    This node runs synchronously within the LangGraph execution.
    The async pause/resume is handled at the WebSocket level:

    1. When this node is reached, the graph streaming is interrupted.
    2. The WebSocket handler detects hitl_pending=True in the state update,
       sends the question to the frontend, and waits for a response.
    3. Once the response arrives, the graph is resumed with hitl_response set.

    In the synchronous path (non-WebSocket), if hitl_response is already
    populated (e.g., from a callback), we just use it and route back.
    """
    hitl_pending = state.get("hitl_pending", False)
    hitl_response = state.get("hitl_response", "")
    origin_node = state.get("hitl_origin_node", "planner")
    question = state.get("hitl_question", "")

    if not hitl_pending:
        # Not actually pending — shouldn't arrive here, route to planner
        logger.warning("HITL node reached but hitl_pending is False")
        return {"next_node": "planner"}

    if hitl_response:
        # Human has responded — record it and route back
        logger.info("HITL response received, routing back to %s", origin_node)

        # Add the HITL exchange to messages for context
        hitl_message = AIMessage(
            content=f"[HITL] Asked: {question}\n[HITL] Human response: {hitl_response}"
        )

        return {
            "messages": [hitl_message],
            "hitl_pending": False,
            "hitl_question": "",
            "hitl_context": "",
            "hitl_reason": "",
            "hitl_response": "",
            "hitl_origin_node": "",
            "next_node": origin_node,
        }

    # No response yet — the graph will be interrupted here.
    # The WebSocket handler picks up hitl_pending=True from state stream,
    # sends the request to the frontend, and resumes the graph with
    # hitl_response filled in.
    #
    # For non-interactive (CLI) mode, return a default response.
    logger.info("HITL waiting for human response (question: %s)", question[:80])
    default_response = "[No human feedback available — agent should proceed with best judgment]"

    hitl_message = AIMessage(
        content=f"[HITL] Asked: {question}\n[HITL] Default response: {default_response}"
    )

    return {
        "messages": [hitl_message],
        "hitl_pending": False,
        "hitl_question": "",
        "hitl_context": "",
        "hitl_reason": "",
        "hitl_response": "",
        "hitl_origin_node": "",
        "next_node": origin_node,
    }
