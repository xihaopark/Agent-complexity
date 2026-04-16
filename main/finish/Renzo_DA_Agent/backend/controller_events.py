from __future__ import annotations

from typing import Any, Dict, Optional


def controller_decision_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = payload.get("decision") or {}
    trace = payload.get("trace") or {}
    return {
        "type": "controller_decision",
        "decision_id": decision.get("decision_id", ""),
        "phase": decision.get("phase", "dialogue"),
        "action_type": (decision.get("action") or {}).get("type", ""),
        "risk_level": decision.get("risk_level", "low"),
        "requires_confirm": bool(decision.get("requires_confirm", False)),
        "reasoning_brief": decision.get("reasoning_brief", ""),
        "fallback_used": bool(decision.get("fallback_used", False)),
        "trace_id": trace.get("trace_id", decision.get("decision_id", "")),
    }


def controller_guardrail_event(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    pending = payload.get("pending_guardrail_action")
    if not isinstance(pending, dict):
        return None
    return {
        "type": "guardrail_confirmation_required",
        "decision_id": pending.get("decision_id", ""),
        "risk_level": pending.get("risk_level", "low"),
        "title": pending.get("title", "Guardrail confirmation required"),
        "summary": pending.get("summary", ""),
        "action": pending.get("action", {}),
    }


def controller_reply_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = payload.get("decision") or {}
    content = decision.get("reply", "") or "Ready."
    pending = payload.get("pending_guardrail_action") if isinstance(payload.get("pending_guardrail_action"), dict) else None
    return {
        "type": "shell_reply",
        "content": content,
        "tone": "professional",
        "concise": True,
        "chips": ["Continue", "Pause", "Stop", "Show details"],
        "pending_action": pending,
        "phase": decision.get("phase", "dialogue"),
        "trace_id": decision.get("decision_id", ""),
    }


def controller_legacy_decision_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = payload.get("decision") or {}
    action = decision.get("action") or {}
    return {
        "type": "shell_decision",
        "trace_id": decision.get("decision_id", ""),
        "phase": decision.get("phase", "dialogue"),
        "intent": action.get("type", "controller"),
        "reasoning_brief": decision.get("reasoning_brief", ""),
        "selected_tools": ["run_engine_turn"] if decision.get("run_engine_prompt") else [],
        "requires_confirm": bool(decision.get("requires_confirm", False)),
        "fallback_used": bool(decision.get("fallback_used", False)),
    }


def run_state_from_result(result: Dict[str, Any]) -> str:
    workflow_status = (result.get("workflow_status") or "").strip().lower()
    if workflow_status == "waiting_user":
        return "waiting_user"
    if workflow_status == "failed":
        return "failed"
    if workflow_status in {"success", "completed"}:
        return "succeeded"
    if result.get("plan_status") == "failed":
        return "failed"
    if result.get("plan_status") == "completed":
        return "succeeded"
    return "running"
