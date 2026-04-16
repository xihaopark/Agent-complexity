from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
FINISH_ROOT = ROOT.parent
os.environ.setdefault("WORKFLOW_POOL_DIR", str(FINISH_ROOT))
os.environ.setdefault("WORKFLOW_SKILLS_DIR", str((ROOT.parent.parent / ".trae" / "skills").resolve()))

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))
import api_gateway as api  # noqa: E402


def _state_signature(state: dict) -> tuple:
    workflow_plan = state.get("workflow_plan") or {}
    steps = workflow_plan.get("steps") or []
    return (
        state.get("workflow_status"),
        state.get("current_step_id"),
        tuple((step.get("id"), step.get("status")) for step in steps),
    )


def main() -> int:
    client = TestClient(api.app)
    workflows = client.get("/api/workflows").json().get("workflows", [])
    workflow = next((item for item in workflows if item.get("id") == "rna-seq-star-deseq2-finish"), None)
    if workflow is None:
        raise SystemExit("workflow rna-seq-star-deseq2-finish not found")

    experiment = client.post(
        "/api/experiments",
        json={
            "name": "Finish workflow run",
            "description": "Run finish star workflow via Renzo agent system",
            "workflow_id": workflow["id"],
        },
    ).json()
    session = client.post(
        f"/api/experiments/{experiment['id']}/sessions",
        json={"name": "star-finish-session"},
    ).json()

    agent = api.RenzoAgent(auto_load_skills=False)
    loaded_skill_specs = agent.load_workflow_skills(
        workflow["id"],
        base_dir=os.environ["WORKFLOW_SKILLS_DIR"],
        clear_existing=True,
    )
    if not loaded_skill_specs:
        raise SystemExit(f"workflow skills for {workflow['id']} not found")
    agent.state["workflow_id_requested"] = workflow["id"]
    agent.state["experiment_id"] = experiment["id"]
    agent.state["session_id"] = session["id"]
    agent.state["artifact_policy"] = "session"
    agent.state["workflow_run_context"] = {
        "run_id": f"wf-{workflow['id']}-{session['id'][:8]}",
        "workflow_id": workflow["id"],
        "engine": workflow["engine"],
        "experiment_id": experiment["id"],
        "session_id": session["id"],
        "execution_mode": "batch",
        "strict_manifest": False,
        "skills_only": True,
        "orchestration_mode": "skills_only",
        "manifest_step_graph_allowed": False,
        "status": "queued",
        "current_step_id": None,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ended_at": None,
        "error_summary": "",
    }
    prompt = (
        "Run the linked workflow from start to finish in IO-only skill orchestration mode. "
        "Use only the workflow-local inputs, the loaded workflow skills, and the observed outputs. "
        "Do not read or rely on any manifest DAG."
    )
    final_state = agent.go(prompt)
    last_signature = _state_signature(final_state)
    for _ in range(20):
        if final_state.get("workflow_status") in {"success", "failed", "error"}:
            break
        next_state = agent.go("Continue executing the current workflow plan.")
        next_signature = _state_signature(next_state)
        final_state = next_state
        if next_signature == last_signature:
            break
        last_signature = next_signature
    serializable_state = dict(final_state)
    serializable_state["messages"] = [{"role": "user", "content": prompt}]
    api.exp_mgr.save_session_state(
        experiment["id"],
        session["id"],
        messages=[{"role": "user", "content": prompt}],
        agent_state=serializable_state,
    )

    events: list[dict] = []
    status_path = ROOT / "data" / "workflow_runs" / f"{session['id']}.agent-run.json"

    session_state = client.get(
        f"/api/experiments/{experiment['id']}/sessions/{session['id']}"
    ).json()
    result = {
        "workflow": workflow["id"],
        "loaded_skill_count": len(loaded_skill_specs),
        "experiment": experiment,
        "session": session,
        "events": events,
        "final_session": session_state,
        "final_state": serializable_state,
    }
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(status_path)
    final_state = session_state.get("agent_state", {})
    print(json.dumps(
        {
            "workflow_status": final_state.get("workflow_status"),
            "current_step_id": final_state.get("current_step_id"),
            "waiting_user": final_state.get("waiting_user"),
        },
        ensure_ascii=False,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
