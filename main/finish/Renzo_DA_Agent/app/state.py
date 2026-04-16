from __future__ import annotations

from typing import Annotated, Any, Dict, List, Optional, TypedDict

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict, total=False):
    """Central state for the agent state machine.

    Every node reads from and writes to this state. Fields are grouped by
    responsibility so that each node only touches the fields it owns.
    """

    # ── Conversation ──────────────────────────────────────────────────
    messages: Annotated[List[BaseMessage], add_messages]

    # ── Goal & Context ────────────────────────────────────────────────
    goal: str
    data_profile: Dict[str, Any]
    artifact_index: List[Dict[str, Any]]
    long_term_summary: str

    # ── Plan ──────────────────────────────────────────────────────────
    plan_version: int
    plan_steps: List[Dict[str, Any]]
    current_step_id: Optional[str]
    plan_status: str  # draft / approved / executing / completed / failed

    # ── Code Generation & Execution ───────────────────────────────────
    code_scratchpad: str
    code_language: str                     # "python" or "r"
    execution_logs: List[Dict[str, Any]]
    installed_packages: List[str]

    # ── QC & Validation ───────────────────────────────────────────────
    qc_results: List[Dict[str, Any]]       # structured QC rule outputs
    validation_result: Dict[str, Any]      # latest validation summary for Planner
    retry_count: int                       # current step retry counter
    max_retries: int                       # max retries allowed (default 2)

    # ── Workflow Execution ────────────────────────────────────────────
    workflow_run_id: Optional[str]
    workflow_status: Optional[str]
    workflow_id_requested: Optional[str]
    workflow_plan: Optional[Dict[str, Any]]
    workflow_run_context: Optional[Dict[str, Any]]  # run_id/workflow_id/engine/... (canonical run context)
    execution_workdir: Optional[str]                # absolute directory where this run writes outputs
    artifact_policy: str                            # session | shared | dual
    orchestration_trace: List[Dict[str, Any]]       # why steps were arranged / selected
    llm_trace: List[Dict[str, Any]]                 # raw LLM prompts and replies

    # ── Human-in-the-Loop (HITL) ──────────────────────────────────────
    hitl_pending: bool                     # True when agent is waiting for human
    hitl_question: str                     # Question for the human
    hitl_context: str                      # Background context for the question
    hitl_reason: str                       # Why the agent needs human input
    hitl_response: str                     # Human's response (filled by frontend)
    hitl_origin_node: str                  # Node that triggered HITL (to return to)

    # ── Know-How / Domain Knowledge ───────────────────────────────────
    know_how_documents: List[Dict[str, Any]]  # Loaded know-how documents
    know_how_context: str                     # Concatenated know-how for LLM context

    # ── Experiment Workspace ──────────────────────────────────────────
    experiment_id: Optional[str]           # Active experiment workspace ID
    session_id: Optional[str]              # Active session within experiment
    dataset_context: str                   # Structured listing of dataset file paths for agent

    # ── Unified Top Controller (new control plane) ───────────────────
    controller_mode: str                   # "legacy" | "unified"
    controller_phase: str                  # dialogue/planning/executing/review/blocked/done
    run_mode: str                          # "async" | "stepwise"
    run_state: str                         # running/background/waiting_user/blocked/failed/succeeded
    pending_guardrail_action: Optional[Dict[str, Any]]
    risk_level: str                        # low/medium/high
    last_controller_decision: Dict[str, Any]
    conversation_loop_count: int
    controller_trace_id: str
    controller_path: str                  # unified|legacy
    confirm_requested: bool
    confirm_reason_risk: str
    loop_guard_triggered: bool
    controller_stats: Dict[str, Any]

    # Deprecated compatibility mirrors for old frontend contract.
    shell_state: Dict[str, Any]

    # ── Data Catalog (maintained by data_analyst node) ────────────────
    data_catalog: List[Dict[str, Any]]     # Per-file profiles for ALL known files
    data_lineage: List[Dict[str, Any]]     # Step -> input files -> output files mapping
    data_analyst_mode: str                 # "init" or "post_step" — tells data_analyst what to do

    # ── Error Pattern Book (session-level learned patterns) ──────────
    error_book: List[Dict[str, Any]]       # Accumulated error→fix patterns

    # ── Answer-only (no execution) ────────────────────────────────────
    answer_only_goal: str                  # When set, responder gives a direct answer without code/artifacts

    # ── Internal Flags ───────────────────────────────────────────────
    _data_ingest_attempted: bool           # Prevents data_ingest <-> planner loop

    # ── Response Attachments (for inline chat rendering) ──────────────
    response_attachments: List[Dict[str, Any]]
    response_qc_table: Optional[List[Dict[str, Any]]]  # QC check rows for table (rule, status, detail)

    # ── Routing ───────────────────────────────────────────────────────
    next_node: str
    terminate: bool

    # ── Prompt version (for A/B or rollback) ──────────────────────────
    prompt_version: Optional[str]  # e.g. "v1", "default"; used by planner/coder to select prompt set


def default_state() -> AgentState:
    return {
        "messages": [],
        "goal": "",
        "data_profile": {},
        "artifact_index": [],
        "long_term_summary": "",
        "plan_version": 0,
        "plan_steps": [],
        "current_step_id": None,
        "plan_status": "draft",
        "code_scratchpad": "",
        "code_language": "python",
        "execution_logs": [],
        "installed_packages": [],
        "qc_results": [],
        "validation_result": {},
        "retry_count": 0,
        "max_retries": 3,
        "workflow_run_id": None,
        "workflow_status": None,
        "workflow_id_requested": None,
        "workflow_plan": None,
        "workflow_run_context": {},
        "execution_workdir": None,
        "artifact_policy": "session",
        "orchestration_trace": [],
        "llm_trace": [],
        "hitl_pending": False,
        "hitl_question": "",
        "hitl_context": "",
        "hitl_reason": "",
        "hitl_response": "",
        "hitl_origin_node": "",
        "know_how_documents": [],
        "know_how_context": "",
        "experiment_id": None,
        "session_id": None,
        "dataset_context": "",
        "controller_mode": "legacy",
        "controller_phase": "dialogue",
        "run_mode": "async",
        "run_state": "background",
        "pending_guardrail_action": None,
        "risk_level": "low",
        "last_controller_decision": {},
        "conversation_loop_count": 0,
        "controller_trace_id": "",
        "controller_path": "unified",
        "confirm_requested": False,
        "confirm_reason_risk": "",
        "loop_guard_triggered": False,
        "controller_stats": {},
        "shell_state": {},
        "data_catalog": [],
        "data_lineage": [],
        "data_analyst_mode": "",
        "error_book": [],
        "_data_ingest_attempted": False,
        "response_attachments": [],
        "next_node": "planner",
        "terminate": False,
    }
