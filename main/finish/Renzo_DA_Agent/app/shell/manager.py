from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from langchain_core.messages import HumanMessage, SystemMessage

from renzo.app.llm import get_llm
from renzo.app.shell.brain import ShellBrain
from renzo.app.shell.memory import default_shell_state, update_key_facts
from renzo.app.shell.policy import PendingAction, control_command_requires_confirm, enforce_confirmation_policy
from renzo.app.shell.rewrite import build_shell_reply, rewrite_engine_summary_for_humans
from renzo.app.shell.router import ShellToolRouter
from renzo.app.shell.schema import ShellDecision


class ConversationShellManager:
    """Top-level shell orchestrator: brain -> policy -> router -> emit."""

    def __init__(self) -> None:
        self.brain = ShellBrain()
        self.router: Optional[ShellToolRouter] = None

    def configure_router(self, router: ShellToolRouter) -> None:
        self.router = router

    def ensure_shell_state(self, session: Dict[str, Any]) -> Dict[str, Any]:
        shell = session.get("shell")
        if isinstance(shell, dict):
            return shell
        shell = default_shell_state()
        session["shell"] = shell
        return shell

    def _new_trace_id(self) -> str:
        return f"trace-{uuid.uuid4().hex[:12]}"

    def _tool_names(self, decision: ShellDecision) -> List[str]:
        return [t.name for t in decision.tool_calls]

    def _build_context(self, session: Dict[str, Any], workflow: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        shell = self.ensure_shell_state(session)
        linked_datasets = session.get("linked_datasets") or []
        linked_dataset_ids = [d.get("id") for d in linked_datasets if isinstance(d, dict) and d.get("id")]
        linked_dataset_names = [d.get("name") for d in linked_datasets if isinstance(d, dict) and d.get("name")]
        return {
            "linked_workflow_id": (workflow or {}).get("id") or "",
            "linked_workflow_name": (workflow or {}).get("name") or "",
            "linked_workflow_steps": [s.get("name") or s.get("id") for s in ((workflow or {}).get("steps") or [])][:8],
            "experiment_id": session.get("experiment_id"),
            "session_id": session.get("session_id"),
            "linked_dataset_ids": linked_dataset_ids,
            "linked_dataset_names": linked_dataset_names[:12],
            "linked_dataset_count": len(linked_dataset_ids),
            "last_intent": shell.get("last_intent", ""),
            "key_facts": shell.get("key_facts", []),
        }

    def _append_trace(
        self,
        shell: Dict[str, Any],
        *,
        trace_id: str,
        decision: ShellDecision,
        fallback_used: bool,
    ) -> Dict[str, Any]:
        trace = {
            "trace_id": trace_id,
            "phase": decision.phase,
            "intent": decision.intent,
            "tool_calls": [tc.model_dump() for tc in decision.tool_calls],
            "requires_confirm": bool(decision.confirm_required),
            "fallback_used": bool(fallback_used),
            "at": uuid.uuid1().time,
        }
        traces = list(shell.get("traces", []))
        traces.append(trace)
        shell["traces"] = traces[-20:]
        shell["last_trace_id"] = trace_id
        shell["last_intent"] = decision.intent
        shell["fallback_used"] = bool(fallback_used)
        shell["last_tool_calls"] = [tc.model_dump() for tc in decision.tool_calls]
        return trace

    def _decision_event(self, trace: Dict[str, Any], decision: ShellDecision) -> Dict[str, Any]:
        return {
            "type": "shell_decision",
            "trace_id": trace["trace_id"],
            "phase": decision.phase,
            "intent": decision.intent,
            "reasoning_brief": decision.reasoning_brief,
            "selected_tools": [tc.name for tc in decision.tool_calls],
            "requires_confirm": bool(decision.confirm_required),
            "fallback_used": bool(trace.get("fallback_used", False)),
        }

    def _proposal_from_action(self, action: PendingAction) -> Dict[str, Any]:
        payload = action.payload if isinstance(action.payload, dict) else {}
        decision = payload.get("decision") if isinstance(payload.get("decision"), dict) else {}
        tool_calls = decision.get("tool_calls") if isinstance(decision.get("tool_calls"), list) else []
        tools = []
        for tc in tool_calls:
            if isinstance(tc, dict) and tc.get("name"):
                tools.append(str(tc.get("name")))
        risks = ["This action will mutate system state."]
        if tools:
            risks.append("Tools to execute: " + ", ".join(tools[:6]))
        return {
            "type": "shell_plan_proposal",
            "action_id": action.action_id,
            "title": action.title,
            "summary": action.summary,
            "steps": action.steps,
            "risks": risks,
            "requires_confirm": True,
        }

    def _needs_interaction_card(self, decision: ShellDecision) -> bool:
        # Non-mutation turns that request user confirmation/supplement/check
        # should still be surfaced as a structured interaction card.
        if decision.confirm_required:
            return False
        if decision.tool_calls:
            return False
        intent = (decision.intent or "").strip().lower()
        if any(k in intent for k in ("clarify", "confirm", "check", "supplement", "need_input", "request_input")):
            return True
        text = (decision.reply_draft or "").strip()
        return "?" in text

    def _legacy_low_risk_force_execute(self, content: str, decision: ShellDecision) -> bool:
        text = (content or "").lower()
        normalized = text.replace("stop asking", "").replace("don't ask", "").replace("dont ask", "")
        strong_execute_phrases = (
            "just do it", "do it now", "run now", "execute now",
            "stop asking", "don't ask", "dont ask",
            "do it", "go ahead", "proceed", "yes", "sure", "ok", "okay",
            "confirmed", "please do", "please run", "run the", "do the", "execute the",
            "run it", "execute it", "go for it", "sounds good",
            "run profiling", "do the profiling", "compute statistics", "run statistics",
            "check the dataset", "profile the", "inspect the",
        )
        strong_execute = any(k in text for k in strong_execute_phrases)
        if not strong_execute:
            return False
        if not decision.tool_calls:
            return False
        if any(tc.name != "run_engine_turn" for tc in decision.tool_calls):
            return False
        # Keep destructive controls guarded.
        if any(k in normalized for k in ("stop", "backtrack", "delete", "drop", "overwrite")):
            return False
        return True

    def _proposal_from_interaction(self, decision: ShellDecision) -> Dict[str, Any]:
        proposal = decision.proposal_card
        title = (proposal.title if proposal else "") or "Input needed before next step"
        summary = (proposal.summary if proposal else "") or (decision.reply_draft.strip()[:260] if decision.reply_draft else "Please confirm or add details so I can continue.")
        steps = proposal.steps if proposal and proposal.steps else [
            "Provide the missing detail, or",
            "Ask me to proceed with explicit assumptions",
            "I will then propose or execute the next concrete step",
        ]
        risks = proposal.risks if proposal and proposal.risks else ["Proceeding without this input may reduce accuracy."]
        return {
            "type": "shell_plan_proposal",
            "title": title,
            "summary": summary,
            "steps": steps,
            "risks": risks,
            "requires_confirm": False,
        }

    def _summarize_tool_results(self, tool_results: List[Dict[str, Any]]) -> str:
        if not tool_results:
            return ""
        lines: List[str] = []
        for item in tool_results[:4]:
            tool = item.get("tool")
            if item.get("ok"):
                result = item.get("result")
                if isinstance(result, list):
                    lines.append(f"- {tool}: {len(result)} item(s)")
                elif isinstance(result, dict) and result.get("id"):
                    lines.append(f"- {tool}: completed ({result.get('id')})")
                else:
                    lines.append(f"- {tool}: completed")
            else:
                lines.append(f"- {tool}: failed ({item.get('error', 'unknown error')})")
        if len(tool_results) > 4:
            lines.append(f"- +{len(tool_results) - 4} more")
        return "\n".join(lines)

    def _humanize_engine_result(self, engine_text: str, workflow_status: str = "", current_step_id: str = "") -> str:
        try:
            llm = get_llm(temperature=0.2, max_tokens=500)
            response = llm.invoke([
                SystemMessage(content=(
                    "Rewrite engine output for a human operator. "
                    "Be concise, natural, and action-oriented. "
                    "Use at most 6 lines. English only."
                )),
                HumanMessage(content=(
                    f"workflow_status={workflow_status}\n"
                    f"current_step_id={current_step_id}\n"
                    f"engine_output:\n{engine_text}"
                )),
            ])
            text = str(response.content or "").strip()
            if text:
                return "\n".join(text.splitlines()[:6])
        except Exception:
            pass
        return rewrite_engine_summary_for_humans(
            engine_text,
            workflow_status=workflow_status,
            current_step_id=current_step_id,
        )

    def _build_run_reply(self, decision: ShellDecision, tool_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        base = decision.reply_draft.strip() or "I completed the requested operation."
        summary = self._summarize_tool_results(tool_results)
        if summary:
            base = f"{base}\n{summary}"
        phase_chip_map = {
            "discovery": ["Show workflows", "Show datasets", "Propose plan"],
            "proposal": ["Confirm plan", "Modify plan", "Show details"],
            "execution": ["Continue", "Pause", "Stop", "Show details"],
            "intervention": ["Retry step", "Backtrack step", "Stop", "Show details"],
            "workflow_management": ["Reuse workflow", "Create workflow", "Show details"],
            "closure": ["Summarize outputs", "Start new run", "Show details"],
        }
        chips = phase_chip_map.get(decision.phase, ["Show details"])
        return build_shell_reply(base, chips=chips)

    def _pending_action_from_decision(self, decision: ShellDecision) -> PendingAction:
        proposal = decision.proposal_card
        tools = [tc.name for tc in decision.tool_calls if (tc.name or "").strip()]
        title = proposal.title if proposal else f"Confirm action: {decision.intent}"
        summary = proposal.summary if proposal else (
            (decision.reply_draft[:240] if decision.reply_draft else "This action will execute tools that modify state.")
        )
        if tools:
            summary = f"{summary}\nPlanned tool calls: {', '.join(tools[:6])}"
        steps = proposal.steps if proposal else [f"Execute tool: {name}" for name in tools] or ["Run selected operation"]
        return PendingAction(
            action_id=f"act-{uuid.uuid4().hex[:10]}",
            action_type=f"decision:{decision.intent}",
            title=title,
            summary=summary,
            steps=steps,
            requires_confirm=True,
            payload={"decision": decision.model_dump(mode="json")},
        )

    def _build_trace_out(self, trace: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "phase": trace.get("phase", "discovery"),
            "intent": trace.get("intent", ""),
            "tool_calls": trace.get("tool_calls", []),
            "requires_confirm": bool(trace.get("requires_confirm", False)),
            "fallback_used": bool(trace.get("fallback_used", False)),
            "trace_id": trace.get("trace_id", ""),
        }

    def handle_event(
        self,
        session: Dict[str, Any],
        *,
        event_type: str,
        content: str = "",
        workflow: Optional[Dict[str, Any]] = None,
        command: str = "",
        target_step_id: Optional[str] = None,
        reason: str = "",
        action_id: str = "",
        approved: bool = False,
        edits: Optional[Dict[str, Any]] = None,
        trace_id: str = "",
    ) -> Dict[str, Any]:
        shell = self.ensure_shell_state(session)
        shell["version"] = int(shell.get("version", 0)) + 1

        if event_type == "shell_tool_result_ack":
            ack_id = (trace_id or "").strip()
            if ack_id:
                acks = list(shell.get("acks", []))
                acks.append(ack_id)
                shell["acks"] = acks[-100:]
            return {
                "reply": None,
                "proposal": None,
                "decision_event": None,
                "memory_hint": None,
                "run_engine_prompt": None,
                "shell_trace": self._build_trace_out({
                    "phase": shell.get("phase", "discovery"),
                    "intent": shell.get("last_intent", ""),
                    "tool_calls": shell.get("last_tool_calls", []),
                    "requires_confirm": bool(shell.get("pending_action")),
                    "fallback_used": bool(shell.get("fallback_used", False)),
                    "trace_id": shell.get("last_trace_id", ""),
                }),
            }

        if event_type == "shell_retry_last":
            retry_content = str(shell.get("last_user_request") or "").strip()
            if not retry_content:
                decision = ShellDecision(
                    phase=shell.get("phase", "discovery"),
                    intent="retry_without_history",
                    reply_draft="There is no previous request to retry in this session.",
                    tool_calls=[],
                    confirm_required=False,
                    reasoning_brief="Retry requested but no last_user_request is available.",
                )
                trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=False)
                reply = build_shell_reply(decision.reply_draft, chips=["Show details"])
                return {
                    "reply": {**reply, "phase": decision.phase, "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }
            content = retry_content
            event_type = "shell_message"

        if event_type in {"shell_message", "message"}:
            if content.strip():
                shell["last_user_request"] = content.strip()
            shell["key_facts"] = update_key_facts(shell, content)
            ctx = self._build_context(session, workflow)
            try:
                decision, fallback_used, _ = self.brain.decide(
                    user_input=content,
                    shell_state=shell,
                    context=ctx,
                )
            except Exception as exc:
                decision = ShellDecision(
                    phase=shell.get("phase", "discovery"),
                    intent="llm_unavailable",
                    reply_draft=(
                        "LLM is currently unavailable, so I did not execute any action. "
                        "Please try again."
                    ),
                    tool_calls=[],
                    confirm_required=False,
                    reasoning_brief=f"LLM unavailable: {str(exc)[:120]}",
                )
                fallback_used = False
                trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=False)
                reply = build_shell_reply(decision.reply_draft, chips=["Try again", "Show details"])
                return {
                    "reply": {**reply, "phase": decision.phase, "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            clarify_like_intent = "clarify" in (decision.intent or "").lower() or "question" in (decision.intent or "").lower()
            no_tools = len(decision.tool_calls) == 0
            if decision.phase == "discovery" and clarify_like_intent and no_tools:
                shell["clarify_streak"] = int(shell.get("clarify_streak", 0)) + 1
            else:
                shell["clarify_streak"] = 0

            # Generic anti-loop guard: after repeated clarification-only turns,
            # force a concrete next action proposal instead of asking again.
            if int(shell.get("clarify_streak", 0)) >= 2 and no_tools:
                decision = ShellDecision(
                    phase="proposal",
                    intent="propose_next_action_after_clarification",
                    reply_draft=(
                        "I have enough context to move forward. "
                        "I prepared a concrete next action so we can proceed."
                    ),
                    tool_calls=[
                        {
                            "name": "run_engine_turn",
                            "arguments": {
                                "prompt": (
                                    "Use the current session context and linked datasets. "
                                    "Proceed with a best-effort analysis for the latest user request, "
                                    "state assumptions explicitly, and produce concrete findings."
                                )
                            },
                        }
                    ],
                    confirm_required=True,
                    proposal_card={
                        "title": "Proposed next action",
                        "summary": "Run a best-effort analysis with explicit assumptions and report concrete findings.",
                        "steps": [
                            "Use linked datasets in current experiment",
                            "Inspect structure and sample rows",
                            "Report findings and assumptions",
                        ],
                        "risks": ["Assumptions may differ from intended study conventions"],
                    },
                    reasoning_brief="Anti-loop guard triggered after repeated clarification-only turns.",
                )
                shell["clarify_streak"] = 0
            decision = enforce_confirmation_policy(decision)
            if self._legacy_low_risk_force_execute(content, decision):
                decision.confirm_required = False
            trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=fallback_used)

            if decision.confirm_required and decision.tool_calls:
                shell["confirm_streak"] = int(shell.get("confirm_streak", 0)) + 1
                if int(shell.get("confirm_streak", 0)) >= 2 and self._legacy_low_risk_force_execute(
                    shell.get("last_user_request", ""),
                    decision,
                ):
                    # Confirm-loop breaker for explicit low-risk execute requests.
                    decision.confirm_required = False
                    shell["confirm_streak"] = 0
                else:
                    action = self._pending_action_from_decision(decision)
                    shell["phase"] = "proposal"
                    shell["pending_action"] = action.to_dict()
                    proposal = self._proposal_from_action(action)
                    reply = build_shell_reply(
                        (decision.reply_draft.strip() or "I prepared an action proposal.")
                        + "\nPlease confirm before I execute mutations.",
                        chips=["Confirm plan", "Modify plan", "Show details"],
                        pending_action=shell["pending_action"],
                    )
                    return {
                        "reply": {**reply, "phase": "proposal", "trace_id": trace["trace_id"]},
                        "proposal": proposal,
                        "decision_event": self._decision_event(trace, decision),
                        "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                        "run_engine_prompt": None,
                        "shell_trace": self._build_trace_out(trace),
                    }

            shell["confirm_streak"] = 0

            if self._needs_interaction_card(decision):
                shell["phase"] = "proposal"
                shell["pending_action"] = None
                proposal = self._proposal_from_interaction(decision)
                reply = build_shell_reply(
                    (decision.reply_draft.strip() or "I need one input from you before I proceed."),
                    chips=["Provide details", "Proceed with assumptions", "Show details"],
                    pending_action=None,
                )
                return {
                    "reply": {**reply, "phase": "proposal", "trace_id": trace["trace_id"]},
                    "proposal": proposal,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            if self.router is None:
                reply = build_shell_reply(
                    "Shell router is not configured. Please check backend configuration.",
                    chips=["Show details"],
                )
                return {
                    "reply": {**reply, "phase": decision.phase, "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            out = self.router.execute(decision=decision, session=session, context=ctx)
            shell["phase"] = decision.phase
            shell["pending_action"] = None
            reply = self._build_run_reply(decision, out.get("tool_results", []))
            return {
                "reply": {**reply, "phase": decision.phase, "trace_id": trace["trace_id"]},
                "proposal": None,
                "decision_event": self._decision_event(trace, decision),
                "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                "run_engine_prompt": out.get("run_engine_prompt"),
                "tool_results": out.get("tool_results", []),
                "shell_trace": self._build_trace_out(trace),
            }

        if event_type == "shell_action_confirm":
            pending = shell.get("pending_action") or {}
            if not pending or pending.get("action_id") != action_id:
                reply = build_shell_reply(
                    "I cannot find that pending action. Please ask me to regenerate the plan.",
                    chips=["Regenerate plan"],
                )
                trace = self._append_trace(
                    shell,
                    trace_id=self._new_trace_id(),
                    decision=ShellDecision(phase=shell.get("phase", "discovery"), intent="confirm_missing_action", reply_draft=reply["content"]),
                    fallback_used=False,
                )
                return {
                    "reply": {**reply, "phase": shell.get("phase", "discovery"), "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, ShellDecision(phase=shell.get("phase", "discovery"), intent="confirm_missing_action", reply_draft=reply["content"])),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            if not approved:
                shell["phase"] = "discovery"
                shell["pending_action"] = None
                decision = ShellDecision(
                    phase="discovery",
                    intent="action_canceled",
                    reply_draft="Action canceled. Tell me what to adjust and I will propose an updated path.",
                )
                trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=False)
                reply = build_shell_reply(decision.reply_draft, chips=["Continue discussion", "Show workflows"])
                return {
                    "reply": {**reply, "phase": "discovery", "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            payload = pending.get("payload") if isinstance(pending.get("payload"), dict) else {}
            decision_data = payload.get("decision") if isinstance(payload.get("decision"), dict) else {}
            decision = ShellDecision.model_validate(decision_data)
            decision.confirm_required = False
            shell["pending_action"] = None
            shell["phase"] = "execution" if decision.phase == "proposal" else decision.phase

            trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=False)
            if self.router is None:
                reply = build_shell_reply("Shell router is not configured.", chips=["Show details"])
                return {
                    "reply": {**reply, "phase": shell.get("phase", "execution"), "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            ctx = self._build_context(session, workflow)
            out = self.router.execute(
                decision=decision,
                session=session,
                context=ctx,
                action_edits=edits if isinstance(edits, dict) else None,
            )
            reply = self._build_run_reply(decision, out.get("tool_results", []))
            return {
                "reply": {**reply, "phase": shell.get("phase", "execution"), "trace_id": trace["trace_id"]},
                "proposal": None,
                "decision_event": self._decision_event(trace, decision),
                "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                "run_engine_prompt": out.get("run_engine_prompt"),
                "tool_results": out.get("tool_results", []),
                "shell_trace": self._build_trace_out(trace),
            }

        if event_type == "shell_control":
            cmd = (command or "").strip().lower()
            if cmd == "reset_to_step":
                return {
                    "reply": None,
                    "proposal": None,
                    "decision_event": None,
                    "memory_hint": None,
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out({"trace_id": "", "phase": "intervention", "intent": "control:reset_to_step"}),
                }
            decision = ShellDecision(
                phase="intervention",
                intent=f"control:{cmd}",
                reply_draft=f"I am ready to apply control command: {cmd}.",
                tool_calls=[
                    {
                        "name": "engine_control",
                        "arguments": {
                            "command": cmd,
                            "target_step_id": target_step_id,
                            "reason": reason,
                        },
                    }
                ],
                confirm_required=False,
                reasoning_brief="Control action: no confirmation required.",
            )
            trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=False)

            if decision.confirm_required:
                action = self._pending_action_from_decision(decision)
                shell["phase"] = "proposal"
                shell["pending_action"] = action.to_dict()
                proposal = self._proposal_from_action(action)
                reply = build_shell_reply(
                    "This control action changes execution state. Please confirm first.",
                    chips=["Confirm control", "Cancel", "Show details"],
                    pending_action=shell["pending_action"],
                )
                return {
                    "reply": {**reply, "phase": "proposal", "trace_id": trace["trace_id"]},
                    "proposal": proposal,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            if self.router is None:
                reply = build_shell_reply("Shell router is not configured.", chips=["Show details"])
                return {
                    "reply": {**reply, "phase": "intervention", "trace_id": trace["trace_id"]},
                    "proposal": None,
                    "decision_event": self._decision_event(trace, decision),
                    "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                    "run_engine_prompt": None,
                    "shell_trace": self._build_trace_out(trace),
                }

            out = self.router.execute(
                decision=decision,
                session=session,
                context=self._build_context(session, workflow),
            )
            reply = self._build_run_reply(decision, out.get("tool_results", []))
            return {
                "reply": {**reply, "phase": "intervention", "trace_id": trace["trace_id"]},
                "proposal": None,
                "decision_event": self._decision_event(trace, decision),
                "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
                "run_engine_prompt": out.get("run_engine_prompt"),
                "tool_results": out.get("tool_results", []),
                "shell_trace": self._build_trace_out(trace),
            }

        reply = build_shell_reply("Unsupported shell event.", chips=["Show details"])
        decision = ShellDecision(phase=shell.get("phase", "discovery"), intent="unsupported_event", reply_draft=reply["content"])
        trace = self._append_trace(shell, trace_id=self._new_trace_id(), decision=decision, fallback_used=False)
        return {
            "reply": {**reply, "phase": shell.get("phase", "discovery"), "trace_id": trace["trace_id"]},
            "proposal": None,
            "decision_event": self._decision_event(trace, decision),
            "memory_hint": {"type": "shell_memory_hint", "key_facts": shell.get("key_facts", [])},
            "run_engine_prompt": None,
            "shell_trace": self._build_trace_out(trace),
        }

    def rewrite_engine_result(
        self,
        session: Dict[str, Any],
        *,
        engine_text: str,
        workflow_status: str = "",
        current_step_id: str = "",
    ) -> Dict[str, Any]:
        shell = self.ensure_shell_state(session)
        if workflow_status in {"success", "failed"}:
            shell["phase"] = "closure"
        elif workflow_status in {"running", "waiting_user"}:
            shell["phase"] = "execution"

        content = self._humanize_engine_result(
            engine_text,
            workflow_status=workflow_status,
            current_step_id=current_step_id,
        )
        if workflow_status == "failed":
            chips = ["Retry step", "Backtrack step", "Stop", "Show details"]
        else:
            chips = ["Continue"]
        reply = build_shell_reply(content, chips=chips)
        reply["phase"] = shell.get("phase", "execution")
        reply["trace_id"] = shell.get("last_trace_id", "")
        return reply

    # Backward-compatible wrappers
    def handle_shell_message(
        self,
        session: Dict[str, Any],
        content: str,
        *,
        workflow: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.handle_event(session, event_type="shell_message", content=content, workflow=workflow)

    def handle_action_confirm(
        self,
        session: Dict[str, Any],
        *,
        action_id: str,
        approved: bool,
        edits: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return self.handle_event(
            session,
            event_type="shell_action_confirm",
            action_id=action_id,
            approved=approved,
            edits=edits,
        )

    def handle_control(
        self,
        session: Dict[str, Any],
        *,
        command: str,
        target_step_id: Optional[str] = None,
        reason: str = "",
    ) -> Dict[str, Any]:
        return self.handle_event(
            session,
            event_type="shell_control",
            command=command,
            target_step_id=target_step_id,
            reason=reason,
        )
