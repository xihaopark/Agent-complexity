from __future__ import annotations

from typing import Dict, List


def default_shell_state() -> Dict:
    return {
        "phase": "discovery",
        "persona": "concise_stable_professional",
        "key_facts": [],
        "pending_action": None,
        "last_user_request": "",
        "clarify_streak": 0,
        "confirm_streak": 0,
        "version": 1,
        "paused": False,
        "traces": [],
        "last_trace_id": "",
        "last_intent": "",
        "fallback_used": False,
        "last_tool_calls": [],
        "acks": [],
    }


def update_key_facts(state: Dict, user_text: str) -> List[str]:
    """Extract and retain compact key facts from user text."""
    text = (user_text or "").strip()
    if not text:
        return list(state.get("key_facts", []))

    facts: List[str] = list(state.get("key_facts", []))
    # Keep memory tiny and useful: only retain a few latest meaningful directives.
    if any(k in text.lower() for k in ["short", "concise", "brief"]):
        facts.append("User prefers concise responses.")
    if any(k in text.lower() for k in ["confirm", "approval"]):
        facts.append("User prefers explicit confirmation before execution.")
    if any(k in text.lower() for k in ["workflow", "experiment"]):
        facts.append("Current task is workflow/experiment driven.")

    lower = text.lower()
    if any(k in lower for k in ["run", "start", "execute", "continue"]):
        facts.append("User issued an execution-oriented request.")
    elif any(k in lower for k in ["plan", "proposal", "roadmap", "steps"]):
        facts.append("User asked for planning support.")
    elif "?" in text:
        facts.append("User asked a clarifying question.")
    else:
        facts.append("User is in discussion mode.")

    # Dedupe while preserving order; keep only recent compact window.
    seen = set()
    compact: List[str] = []
    for f in facts:
        if f in seen:
            continue
        seen.add(f)
        compact.append(f)
    return compact[-8:]
