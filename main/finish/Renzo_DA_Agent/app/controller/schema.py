from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


ControllerMode = Literal["legacy", "unified"]
ControllerPhase = Literal["dialogue", "planning", "executing", "review", "blocked", "done"]
RunMode = Literal["async", "stepwise"]
RiskLevel = Literal["low", "medium", "high"]
ControllerActionType = Literal[
    "execute_step",
    "ask_user",
    "confirm_guardrail",
    "summarize_progress",
    "pause_run",
]


class ControllerAction(BaseModel):
    type: ControllerActionType
    prompt: str = ""
    details: Dict[str, Any] = Field(default_factory=dict)


class GuardrailPolicy(BaseModel):
    require_confirm_for_medium: bool = False
    require_confirm_for_high: bool = True
    medium_risk_controls: List[str] = Field(default_factory=lambda: ["pause", "retry_step"])
    high_risk_controls: List[str] = Field(default_factory=lambda: ["stop", "backtrack_step", "delete", "overwrite"])


class ControllerDecision(BaseModel):
    decision_id: str
    mode: ControllerMode = "unified"
    phase: ControllerPhase = "dialogue"
    action: ControllerAction
    risk_level: RiskLevel = "low"
    requires_confirm: bool = False
    reply: str = ""
    reasoning_brief: str = ""
    state_patch: Dict[str, Any] = Field(default_factory=dict)
    run_engine_prompt: Optional[str] = None
    fallback_used: bool = False
    fallback_reason: str = ""


class PendingGuardrailAction(BaseModel):
    decision_id: str
    title: str
    summary: str
    action: ControllerAction
    risk_level: RiskLevel
    run_engine_prompt: str = ""
    edits: Dict[str, Any] = Field(default_factory=dict)


class ControllerTrace(BaseModel):
    trace_id: str
    phase: ControllerPhase
    action: ControllerActionType
    risk_level: RiskLevel
    requires_confirm: bool
    fallback_used: bool = False
