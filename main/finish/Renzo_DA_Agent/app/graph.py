from __future__ import annotations

from langgraph.graph import END, StateGraph

from renzo.app.state import AgentState
from renzo.app.nodes.router import router_node
from renzo.app.nodes.planner import planner_node
from renzo.app.nodes.data_ingest import data_ingest_node
from renzo.app.nodes.preprocess import preprocess_node
from renzo.app.nodes.coder import coder_node
from renzo.app.nodes.executor import executor_node
from renzo.app.nodes.step_validate import step_validate_node
from renzo.app.nodes.qc import qc_node
from renzo.app.nodes.step_finalize import step_finalize_node
from renzo.app.nodes.responder import responder_node
from renzo.app.nodes.hitl import hitl_node
from renzo.app.nodes.data_analyst import data_analyst_node


def build_graph():
    """Build the agent state machine graph.

    Flow (happy path):
        Router -> Planner -> DataIngest -> DataAnalyst(init) -> Planner -> Coder
               -> Executor -> StepValidate -> DataAnalyst(post_step) -> QC
               -> StepFinalize -> Responder -> END

    Flow (retry on failure):
        StepValidate --[fail, retryable]--> Coder  (regenerate code)
        StepValidate --[fail, terminal]---> StepFinalize (give up)

    Flow (QC failure):
        QC --[fail]--> Planner  (replan / adjust)

    Flow (Human-in-the-Loop):
        Planner/Coder/QC --[uncertainty]--> HITL --[response]--> originating node

    Nodes:
    - router:         Event intake and dispatch (hub)
    - planner:        Central decision maker — creates/revises plans via LLM
    - data_ingest:    Load and profile data files
    - preprocess:     Data cleaning (placeholder)
    - coder:          LLM-powered code generation (Python + R)
    - executor:       Execute code (Python/R) or workflow steps
    - step_validate:  Check execution results, decide retry vs proceed
    - qc:             Run QC rule chain on outputs
    - step_finalize:  Register artifacts, mark step done
    - responder:      LLM-powered user-facing summary
    - hitl:           Human-in-the-Loop interaction point
    """
    graph = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────
    graph.add_node("router", router_node)
    graph.add_node("planner", planner_node)
    graph.add_node("data_ingest", data_ingest_node)
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("coder", coder_node)
    graph.add_node("executor", executor_node)
    graph.add_node("step_validate", step_validate_node)
    graph.add_node("qc", qc_node)
    graph.add_node("step_finalize", step_finalize_node)
    graph.add_node("responder", responder_node)
    graph.add_node("hitl", hitl_node)
    graph.add_node("data_analyst", data_analyst_node)

    # ── Entry point ───────────────────────────────────────────────────
    graph.set_entry_point("router")

    # ── Router: conditional dispatch based on next_node ───────────────
    def route(state: AgentState):
        if state.get("terminate"):
            return END
        return state.get("next_node", "planner")

    graph.add_conditional_edges("router", route)

    # ── Fixed edges: every node returns to router except the
    #    execution pipeline (executor -> step_validate) and terminal ───
    graph.add_edge("planner", "router")
    graph.add_edge("data_ingest", "router")
    graph.add_edge("preprocess", "router")
    graph.add_edge("coder", "router")

    # Execution pipeline: executor -> step_validate (always)
    graph.add_edge("executor", "step_validate")

    # step_validate decides where to go via next_node -> router
    graph.add_edge("step_validate", "router")

    # QC decides where to go (pass -> step_finalize, fail -> planner)
    graph.add_edge("qc", "router")

    # step_finalize -> router (usually routes to responder)
    graph.add_edge("step_finalize", "router")

    # HITL -> router (routes back to origin node after human responds)
    graph.add_edge("hitl", "router")

    # data_analyst -> router (routes to planner after init, or qc after post_step)
    graph.add_edge("data_analyst", "router")

    # responder terminates
    graph.add_edge("responder", END)

    return graph.compile()
