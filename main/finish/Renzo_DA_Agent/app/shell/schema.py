from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ShellToolCall(BaseModel):
    name: str = ""
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ProposalCard(BaseModel):
    title: str
    summary: str
    steps: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)


class ShellDecision(BaseModel):
    phase: str = "discovery"
    intent: str = "general_discussion"
    reply_draft: str = ""
    tool_calls: List[ShellToolCall] = Field(default_factory=list)
    confirm_required: bool = False
    proposal_card: Optional[ProposalCard] = None
    reasoning_brief: str = ""


class ShellTrace(BaseModel):
    trace_id: str
    phase: str
    intent: str
    tool_calls: List[ShellToolCall] = Field(default_factory=list)
    requires_confirm: bool = False
    fallback_used: bool = False


class ShellPhaseState(BaseModel):
    phase: str = "discovery"
    persona: str = "concise_stable_professional"
    key_facts: List[str] = Field(default_factory=list)
    pending_action: Optional[Dict[str, Any]] = None
    version: int = 1
    paused: bool = False
    traces: List[Dict[str, Any]] = Field(default_factory=list)
    last_trace_id: str = ""
    last_intent: str = ""
    fallback_used: bool = False
    last_tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    acks: List[str] = Field(default_factory=list)
