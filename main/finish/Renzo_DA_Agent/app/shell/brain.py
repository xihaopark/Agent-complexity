from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Tuple

from langchain_core.messages import HumanMessage, SystemMessage

from renzo.app.llm import get_llm
from renzo.app.shell.schema import ShellDecision

_SYSTEM_PROMPT = """You are the Conversation Shell for an experiment engine.

Goals:
- Be a natural, professional, collaborative assistant.
- Decide current phase and intent.
- Select tool calls only when helpful.
- Never execute code directly. Use tools.
- Keep replies concise but not robotic.
- Output must be valid JSON matching schema fields exactly.

Rules:
- Mutation actions MUST set confirm_required=true EXCEPT when the user has given clear go-ahead (e.g. "do it", "go ahead", "run it", "proceed", "yes") or the request is read-only (profile, statistics, inspect, check, schema). For those, set confirm_required=false so execution runs immediately.
- Mutation tools include: create_workflow, start_experiment_from_workflow, run_engine_turn, engine_control, link_experiment.
- If uncertain, ask a clarifying question in reply_draft and use no mutation tools.
- Always produce English output.
- reasoning_brief should be short and factual.
- When user asks about datasets/files without an explicit scope, default to the current experiment/session context.
- If context includes linked_dataset_ids, prefer listing those first (scope=linked) before asking for scope clarification.
- Be proactive: when the user gives an actionable request, choose sensible defaults and move forward instead of repeatedly asking for permission. Do not ask "Confirm and I'll execute" when the user has already said to do it or when the task is profile/statistics/inspect.
- Clarification budget: ask at most one clarification question before proposing or taking the next concrete action.
- Do not repeat clarification questions already answered in this session context.
- Avoid conversational loops. If user intent is clear enough (>70%), produce tool_calls and progress.
- For requests like preview/check/schema/metadata/sample/inspect/profile/statistics, prefer action using current linked datasets by default and set confirm_required=false.
- If user asks to use all data from currently linked datasets, treat that as a direct execution intent with explicit assumptions, not a scope loop.

JSON schema fields:
phase, intent, reply_draft, tool_calls, confirm_required, proposal_card, reasoning_brief.
Return JSON only. Do not include markdown.
"""

_REPAIR_PROMPT = """Fix the following into valid JSON only.
Required top-level keys:
- phase (string)
- intent (string)
- reply_draft (string)
- tool_calls (array of {name:string, arguments:object})
- confirm_required (boolean)
- proposal_card (object|null)
- reasoning_brief (string)
Output JSON only, no markdown.
"""

_VALID_PHASES = {
    "discovery",
    "proposal",
    "execution",
    "intervention",
    "workflow_management",
    "closure",
}

_VALID_TOOLS = {
    "list_workflows",
    "get_workflow",
    "create_workflow",
    "start_experiment_from_workflow",
    "run_engine_turn",
    "engine_control",
    "list_datasets",
    "link_experiment",
}


class ShellBrain:
    """LLM decision layer for the shell orchestration manager."""

    def __init__(self) -> None:
        self.allow_fallback = os.environ.get("SHELL_FALLBACK_RULES", "false").lower() in {"1", "true", "yes", "on"}

    def _extract_json(self, text: str) -> str:
        raw = (text or "").strip()
        if raw.startswith("```"):
            raw = re.sub(r"^```(?:json)?\\s*", "", raw)
            raw = re.sub(r"\\s*```$", "", raw)
            raw = raw.strip()

        if raw.startswith("{") and raw.endswith("}"):
            return raw

        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            return match.group(0)
        raise ValueError("No JSON object found in LLM output")

    def _normalize_phase(self, value: Any) -> str:
        phase = str(value or "").strip().lower()
        aliases = {
            "discover": "discovery",
            "discussion": "discovery",
            "execute": "execution",
            "run": "execution",
            "intervene": "intervention",
            "workflow": "workflow_management",
            "management": "workflow_management",
            "close": "closure",
            "final": "closure",
        }
        if phase in _VALID_PHASES:
            return phase
        if phase in aliases:
            return aliases[phase]
        return "discovery"

    def _normalize_tool_calls(self, value: Any) -> list[dict]:
        out: list[dict] = []
        calls = value if isinstance(value, list) else []
        for raw in calls:
            if isinstance(raw, str):
                name = raw.strip()
                args: Dict[str, Any] = {}
            elif isinstance(raw, dict):
                name = str(raw.get("name") or "").strip()
                args = raw.get("arguments") if isinstance(raw.get("arguments"), dict) else {}
            else:
                continue
            if not name:
                continue
            if name not in _VALID_TOOLS:
                # keep unknown tools out of routing path
                continue
            out.append({"name": name, "arguments": args})
        return out[:8]

    def _normalize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        proposal = payload.get("proposal_card")
        if not isinstance(proposal, dict):
            proposal = None
        else:
            proposal = {
                "title": str(proposal.get("title") or "Proposed action"),
                "summary": str(proposal.get("summary") or ""),
                "steps": [str(x) for x in (proposal.get("steps") or []) if str(x).strip()],
                "risks": [str(x) for x in (proposal.get("risks") or []) if str(x).strip()],
            }
        return {
            "phase": self._normalize_phase(payload.get("phase")),
            "intent": str(payload.get("intent") or "general_discussion"),
            "reply_draft": str(payload.get("reply_draft") or ""),
            "tool_calls": self._normalize_tool_calls(payload.get("tool_calls")),
            "confirm_required": bool(payload.get("confirm_required", False)),
            "proposal_card": proposal,
            "reasoning_brief": str(payload.get("reasoning_brief") or ""),
        }

    def _parse_decision_payload(self, text: str) -> ShellDecision:
        payload = json.loads(self._extract_json(text))
        if not isinstance(payload, dict):
            raise ValueError("Decision payload is not an object")
        normalized = self._normalize_payload(payload)
        return ShellDecision.model_validate(normalized)

    def _repair_and_parse(self, broken_text: str) -> ShellDecision:
        llm = get_llm(temperature=0.0, max_tokens=800)
        repaired = llm.invoke([
            SystemMessage(content=_REPAIR_PROMPT),
            HumanMessage(content=broken_text),
        ])
        return self._parse_decision_payload(str(repaired.content))

    def _infer_conversation_mode(self, text: str) -> Dict[str, Any]:
        lower = (text or "").lower()
        out: Dict[str, Any] = {
            "requested_execution": False,
            "requested_plan": False,
            "requested_recommendation": False,
            "asked_question": "?" in (text or ""),
            "mentioned_constraints": False,
        }
        if any(x in lower for x in ["run", "start", "execute", "go ahead", "continue"]):
            out["requested_execution"] = True
        if any(x in lower for x in ["plan", "proposal", "roadmap", "steps"]):
            out["requested_plan"] = True
        if any(x in lower for x in ["recommend", "advice", "suggest", "best practice"]):
            out["requested_recommendation"] = True
        if any(x in lower for x in ["constraint", "deadline", "timeline", "budget", "accuracy", "quality", "risk"]):
            out["mentioned_constraints"] = True
        return out

    def _fallback_decision(self, user_input: str, shell_state: Dict[str, Any], error: str) -> ShellDecision:
        lowered = (user_input or "").lower()
        phase = shell_state.get("phase") or "discovery"
        inferred = self._infer_conversation_mode(user_input)

        if inferred["requested_execution"]:
            return ShellDecision(
                phase="proposal",
                intent="request_execution",
                reply_draft=(
                    "I can execute this through the engine with step-by-step control. "
                    "I prepared a guarded execution proposal for your confirmation."
                ),
                tool_calls=[{"name": "run_engine_turn", "arguments": {"prompt": "Start the linked workflow and execute the first step."}}],
                confirm_required=True,
                proposal_card={
                    "title": "Execution proposal",
                    "summary": "Start the linked workflow with step-by-step control.",
                    "steps": ["Validate context", "Run next step", "Report outputs"],
                    "risks": ["Long-running step may require manual continue"],
                },
                reasoning_brief=f"Fallback mode due to LLM issue: {error[:120]}",
            )

        if inferred["requested_plan"]:
            return ShellDecision(
                phase="proposal",
                intent="draft_plan",
                reply_draft=(
                    "I can draft an execution plan now and keep it editable before any run. "
                    "I will include assumptions, risks, and checkpoints."
                ),
                tool_calls=[],
                confirm_required=False,
                proposal_card={
                    "title": "Draft plan outline",
                    "summary": "Scope, map inputs, execute stepwise, validate outputs, compare against expectations.",
                    "steps": ["Scope and constraints", "Input profiling", "Transformation steps", "QC and reconciliation", "Final outputs"],
                    "risks": ["Missing metadata", "Ambiguous derivations", "Inconsistent variable conventions"],
                },
                reasoning_brief=f"Plan-first fallback due to LLM issue: {error[:120]}",
            )

        if inferred["requested_recommendation"] or inferred["asked_question"] or inferred["mentioned_constraints"]:
            return ShellDecision(
                phase="discovery",
                intent="consultative_discussion",
                reply_draft=(
                    "I can help compare options and suggest a concrete path. "
                    "Share your objective, constraints, and preferred tradeoff (speed vs. rigor), "
                    "and I will propose a recommendation with rationale."
                ),
                tool_calls=[
                    {"name": "list_workflows", "arguments": {}},
                    {"name": "list_datasets", "arguments": {}},
                ],
                confirm_required=False,
                reasoning_brief=f"Consultative fallback due to LLM issue: {error[:120]}",
            )

        return ShellDecision(
            phase=phase if phase in {"discovery", "proposal", "execution", "intervention", "workflow_management", "closure"} else "discovery",
            intent="general_discussion",
            reply_draft=(
                "I can work with you as an orchestration partner, not just a runner. "
                "If you share your target outputs, constraints, and success criteria, I will suggest options and only execute after confirmation."
            ),
            tool_calls=[],
            confirm_required=False,
            reasoning_brief=f"Fallback mode due to LLM issue: {error[:120]}",
        )

    def decide(
        self,
        *,
        user_input: str,
        shell_state: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[ShellDecision, bool, str]:
        """Return (decision, fallback_used, fallback_reason)."""
        request = {
            "user_input": user_input,
            "shell_state": {
                "phase": shell_state.get("phase"),
                "key_facts": shell_state.get("key_facts", []),
                "pending_action": shell_state.get("pending_action"),
                "paused": shell_state.get("paused", False),
                "last_intent": shell_state.get("last_intent", ""),
            },
            "context": context,
        }
        try:
            llm = get_llm(temperature=0.2, max_tokens=1200)
            response = llm.invoke([
                SystemMessage(content=_SYSTEM_PROMPT),
                HumanMessage(content=json.dumps(request, ensure_ascii=True)),
            ])
            try:
                decision = self._parse_decision_payload(str(response.content))
            except Exception:
                decision = self._repair_and_parse(str(response.content))
            return decision, False, ""
        except Exception as exc:
            reason = str(exc)
            if not self.allow_fallback:
                raise RuntimeError(reason)
            return self._fallback_decision(user_input, shell_state, reason), True, reason
