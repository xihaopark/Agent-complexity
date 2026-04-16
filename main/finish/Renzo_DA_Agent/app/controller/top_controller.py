from __future__ import annotations

import json
import os
import re
import uuid
from typing import Any, Dict, Optional, Tuple

from langchain_core.messages import HumanMessage, SystemMessage

from renzo.app.llm import get_llm
from renzo.app.controller.schema import (
    ControllerAction,
    ControllerDecision,
    ControllerTrace,
    GuardrailPolicy,
    PendingGuardrailAction,
)

_SYSTEM_PROMPT = """You are Top Controller for an experiment engine.
Return JSON with keys exactly:
phase, action_type, run_engine_prompt, ask_user, risk_level, reasoning_brief.
Allowed phase: dialogue, planning, executing, review, blocked, done.
Allowed action_type: execute_step, ask_user, confirm_guardrail, summarize_progress, pause_run.
Allowed risk_level: low, medium, high.
If user clearly asks to run/continue/execute/do/proceed (e.g. run profiling, do it, go ahead, compute statistics), set action_type=execute_step and provide run_engine_prompt with the actual request. Use risk_level=low for read-only or analysis tasks (profile, statistics, inspect, check, schema, sample). Do not ask for confirmation for low-risk execution—execute immediately.
Do not ask repeated clarification if user intent is clear. Prefer executing over asking.
JSON only.
"""


class TopController:
    """Unified conversation + execution controller."""

    def __init__(self, *, policy: Optional[GuardrailPolicy] = None) -> None:
        self.policy = policy or GuardrailPolicy()
        self.llm_enabled = os.environ.get("TOP_CONTROLLER_LLM_ENABLED", "true").lower() in {"1", "true", "yes", "on"}

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:12]}"

    def _extract_json(self, text: str) -> Dict[str, Any]:
        raw = (text or "").strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\\s*", "", raw)
            raw = re.sub(r"\\s*```$", "", raw).strip()
        if not raw.startswith("{"):
            m = re.search(r"\{[\s\S]*\}", raw)
            if m:
                raw = m.group(0)
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("Controller payload must be an object")
        return data

    def _is_execution_intent(self, text: str) -> bool:
        lower = (text or "").lower().strip()
        phrases = (
            "run", "execute", "start", "continue", "go ahead", "proceed", "next step", "retry",
            "do it", "just do it", "do it now", "run now", "execute now", "yes", "sure", "ok", "okay",
            "confirmed", "please do", "please run", "run the", "do the", "execute the", "run it",
            "go for it", "sounds good", "stop asking", "don't ask", "dont ask",
        )
        return any(k in lower for k in phrases)

    def _is_read_only_request(self, text: str) -> bool:
        """True if the request is clearly read-only (profile, stats, inspect) — should not require confirmation."""
        lower = (text or "").lower()
        return any(
            k in lower
            for k in ("profile", "profiling", "statistics", "stats", "inspect", "check dataset", "check the data", "schema", "sample", "metadata", "row count", "column count", "missingness", "summary", "summaries")
        )

    def _looks_like_question(self, text: str) -> bool:
        """True if the input looks like a knowledge/how-to question that the agent should answer."""
        lower = (text or "").strip().lower()
        if len(lower) < 10:
            return False
        question_phrases = (
            "how to", "how do", "how can", "what is", "what are", "why ", "when ", "where ",
            "explain", "describe", "tell me", "can you tell", "could you", "guide", "overview",
            "sdtm", "adam", "adae", "adsl", "generate", "create", "document",
        )
        return any(p in lower for p in question_phrases)

    def _is_control_intent(self, text: str) -> Optional[str]:
        lower = (text or "").lower().strip()
        if "stop asking" in lower or "don't ask" in lower or "dont ask" in lower:
            return None
        if any(k in lower for k in ["stop", "terminate", "halt"]):
            return "stop"
        if any(k in lower for k in ["pause", "hold"]):
            return "pause"
        if "backtrack" in lower or "go back" in lower:
            return "backtrack_step"
        if "retry" in lower:
            return "retry_step"
        return None

    def _risk_for_input(self, text: str, explicit_control: Optional[str] = None) -> str:
        control = explicit_control or self._is_control_intent(text)
        if control in set(self.policy.high_risk_controls):
            return "high"
        if control in set(self.policy.medium_risk_controls):
            return "medium"
        if any(k in (text or "").lower() for k in ["delete", "drop", "overwrite", "remove"]):
            return "high"
        return "low"

    def _requires_confirm(self, risk_level: str) -> bool:
        if risk_level == "high":
            return bool(self.policy.require_confirm_for_high)
        if risk_level == "medium":
            return bool(self.policy.require_confirm_for_medium)
        return False

    def _llm_decide(self, user_input: str, context: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
        if not self.llm_enabled:
            return None, "llm_disabled"
        try:
            llm = get_llm(temperature=0.0, max_tokens=600)
            response = llm.invoke([
                SystemMessage(content=_SYSTEM_PROMPT),
                HumanMessage(content=json.dumps({"user_input": user_input, "context": context}, ensure_ascii=True)),
            ])
            return self._extract_json(str(response.content)), ""
        except Exception as exc:
            return None, str(exc)

    def _fallback_decide(self, user_input: str, shell_state: Dict[str, Any]) -> Dict[str, Any]:
        loop_count = int(shell_state.get("conversation_loop_count", 0) or 0)
        control = self._is_control_intent(user_input)
        if control:
            prompt_map = {
                "stop": "stop this workflow run and summarize current status.",
                "pause": "pause",
                "retry_step": "retry current step",
                "backtrack_step": "go back to previous step and rerun from there",
            }
            return {
                "phase": "executing",
                "action_type": "execute_step",
                "run_engine_prompt": prompt_map.get(control, "continue"),
                "ask_user": "",
                "risk_level": self._risk_for_input(user_input, control),
                "reasoning_brief": "Deterministic control fallback.",
            }
        if self._is_execution_intent(user_input):
            return {
                "phase": "executing",
                "action_type": "execute_step",
                "run_engine_prompt": user_input.strip() or "continue",
                "ask_user": "",
                "risk_level": self._risk_for_input(user_input),
                "reasoning_brief": "Deterministic execution fallback.",
            }
        if loop_count >= 1:
            return {
                "phase": "planning",
                "action_type": "execute_step",
                "run_engine_prompt": "Use current context and linked datasets. Proceed with explicit assumptions and produce concrete progress.",
                "ask_user": "",
                "risk_level": "low",
                "reasoning_brief": "Anti-loop forced execution proposal.",
            }
        # Clear question / how-to / knowledge request: hand to engine so the agent can answer (e.g. SDTM/ADaM, how-to).
        if self._looks_like_question(user_input):
            return {
                "phase": "dialogue",
                "action_type": "execute_step",
                "run_engine_prompt": user_input.strip(),
                "ask_user": "",
                "risk_level": "low",
                "reasoning_brief": "Question or how-to: hand to engine to answer.",
            }
        return {
            "phase": "dialogue",
            "action_type": "ask_user",
            "run_engine_prompt": "",
            "ask_user": "I can proceed now with default assumptions, or you can add one missing constraint.",
            "risk_level": "low",
            "reasoning_brief": "Needs one clarification.",
        }

    def _build_pending_action(self, decision: ControllerDecision) -> PendingGuardrailAction:
        return PendingGuardrailAction(
            decision_id=decision.decision_id,
            title="Guardrail confirmation required",
            summary=decision.reply or "This action requires confirmation.",
            action=decision.action,
            risk_level=decision.risk_level,
            run_engine_prompt=decision.run_engine_prompt or "",
        )

    def _sync_run_mode_into_workflow_context(self, state: Dict[str, Any]) -> None:
        run_ctx = state.get("workflow_run_context")
        if not isinstance(run_ctx, dict):
            return
        run_mode = str(state.get("run_mode") or "async").strip().lower()
        run_ctx["execution_mode"] = "interactive" if run_mode == "stepwise" else "batch"
        state["workflow_run_context"] = run_ctx

    def handle_turn(
        self,
        *,
        session: Dict[str, Any],
        user_input: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        state = session.setdefault("state", {})
        state["controller_mode"] = "unified"
        state["run_mode"] = state.get("run_mode") or "async"
        loop_count = int(state.get("conversation_loop_count", 0) or 0)

        payload, llm_error = self._llm_decide(user_input, context)
        fallback_used = False
        fallback_reason = ""
        if payload is None:
            payload = self._fallback_decide(user_input, state)
            fallback_used = True
            fallback_reason = llm_error or "fallback"

        phase = str(payload.get("phase") or "dialogue")
        action_type = str(payload.get("action_type") or "ask_user")
        run_engine_prompt = str(payload.get("run_engine_prompt") or "").strip() or None
        ask_user = str(payload.get("ask_user") or "").strip()
        # If controller said ask_user but the input is clearly a question (e.g. "How to use SDTM to generate ADaM?"), hand to engine to answer.
        if action_type == "ask_user" and self._looks_like_question(user_input):
            action_type = "execute_step"
            run_engine_prompt = user_input.strip()
            ask_user = ""
            phase = "dialogue"
        risk_level = str(payload.get("risk_level") or self._risk_for_input(user_input)).lower()
        if risk_level not in {"low", "medium", "high"}:
            risk_level = "low"
        # Read-only requests (profile, statistics, inspect) are always low risk and must not block on confirmation.
        if self._is_read_only_request(user_input):
            risk_level = "low"
        requires_confirm = self._requires_confirm(risk_level)
        # Explicit "continue" (e.g. user clicked Continue chip): never ask for confirmation.
        if (user_input or "").strip().lower() == "continue":
            requires_confirm = False
        # Clear execution intent or explicit go-ahead: execute immediately, do not ask for confirmation.
        # Do not bypass when user is requesting a control action (stop, pause, backtrack).
        control_intent = self._is_control_intent(user_input)
        if (
            action_type == "execute_step"
            and run_engine_prompt
            and not control_intent
            and (self._is_execution_intent(user_input) or self._is_read_only_request(user_input))
        ):
            requires_confirm = False

        if action_type == "ask_user" and not ask_user:
            ask_user = "Please share one missing constraint, or tell me to proceed with assumptions."

        # Clarification budget: at most one clarification turn for same intent.
        if action_type == "ask_user":
            loop_count += 1
        else:
            loop_count = 0

        loop_guard_triggered = False
        if loop_count >= 2:
            action_type = "execute_step"
            phase = "planning"
            run_engine_prompt = run_engine_prompt or "Proceed with explicit assumptions and execute the next safe step."
            ask_user = ""
            requires_confirm = self._requires_confirm("low")
            risk_level = "low"
            loop_guard_triggered = True

        action_prompt = run_engine_prompt if action_type == "execute_step" else ask_user
        action = ControllerAction(type=action_type, prompt=action_prompt)
        decision = ControllerDecision(
            decision_id=self._new_id("dec"),
            phase=phase if phase in {"dialogue", "planning", "executing", "review", "blocked", "done"} else "dialogue",
            action=action,
            risk_level=risk_level,  # type: ignore[arg-type]
            requires_confirm=bool(requires_confirm and action_type == "execute_step"),
            reply=(
                "I will execute the next step now." if action_type == "execute_step" and not requires_confirm else
                "I prepared the next action. Please confirm to continue." if action_type == "execute_step" else
                ask_user
            ),
            reasoning_brief=str(payload.get("reasoning_brief") or "Unified controller decision."),
            run_engine_prompt=run_engine_prompt,
            fallback_used=fallback_used,
            fallback_reason=fallback_reason,
            state_patch={
                "controller_mode": "unified",
                "controller_phase": phase,
                "risk_level": risk_level,
                "conversation_loop_count": loop_count,
                "run_mode": state.get("run_mode") or "async",
                "run_state": "running" if action_type == "execute_step" else "background",
                "loop_guard_triggered": loop_guard_triggered,
            },
        )

        state.update(decision.state_patch)
        state["last_controller_decision"] = decision.model_dump(mode="json")
        state["controller_trace_id"] = decision.decision_id
        self._sync_run_mode_into_workflow_context(state)

        pending = state.get("pending_guardrail_action")
        if decision.requires_confirm:
            # Repeated confirm suppression for same action prompt.
            if isinstance(pending, dict) and pending.get("run_engine_prompt") == (decision.run_engine_prompt or ""):
                decision.reply = "Pending confirmation already exists. Confirm it to continue."
            else:
                state["pending_guardrail_action"] = self._build_pending_action(decision).model_dump(mode="json")

        trace = ControllerTrace(
            trace_id=decision.decision_id,
            phase=decision.phase,
            action=decision.action.type,
            risk_level=decision.risk_level,
            requires_confirm=decision.requires_confirm,
            fallback_used=decision.fallback_used,
        )

        run_prompt = None
        if decision.action.type == "execute_step" and not decision.requires_confirm:
            run_prompt = decision.run_engine_prompt
            state["pending_guardrail_action"] = None
            state["controller_phase"] = "executing"
            state["run_state"] = "running"

        return {
            "decision": decision.model_dump(mode="json"),
            "trace": trace.model_dump(mode="json"),
            "run_engine_prompt": run_prompt,
            "pending_guardrail_action": state.get("pending_guardrail_action"),
        }

    def handle_guardrail_confirm(
        self,
        *,
        session: Dict[str, Any],
        decision_id: str,
        approved: bool,
        edits: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        state = session.setdefault("state", {})
        pending = state.get("pending_guardrail_action")
        if not isinstance(pending, dict) or pending.get("decision_id") != decision_id:
            return {
                "error": "missing_pending_action",
                "reply": "No matching pending guardrail action. Please request a new action.",
                "run_engine_prompt": None,
            }

        if not approved:
            state["pending_guardrail_action"] = None
            state["controller_phase"] = "dialogue"
            state["run_state"] = "background"
            return {
                "reply": "Action canceled. Share adjustments and I will propose the next safe action.",
                "run_engine_prompt": None,
            }

        run_prompt = str((edits or {}).get("engine_prompt") or pending.get("run_engine_prompt") or "").strip()
        state["pending_guardrail_action"] = None
        state["controller_phase"] = "executing"
        state["run_state"] = "running"
        state["risk_level"] = pending.get("risk_level", "low")
        state["controller_trace_id"] = decision_id
        self._sync_run_mode_into_workflow_context(state)
        return {
            "reply": "Confirmed. Executing now.",
            "run_engine_prompt": run_prompt or None,
        }
