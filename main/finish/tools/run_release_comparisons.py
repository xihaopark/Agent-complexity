from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RENZO_ROOT = ROOT / "Renzo_DA_Agent"
PLAN_JSON = ROOT / "BENCHMARK_RUN_PLAN.json"
SANDBOX_STATUS_JSON = ROOT / "SANDBOX_ENV_STATUS.json"
EVALUABILITY_STATUS_JSON = ROOT / "WORKFLOW_EVALUABILITY_STATUS.json"
COMPARISON_SCRIPT = RENZO_ROOT / "scripts" / "run_finish_workflow_comparison.py"
SUMMARY_SCRIPT = RENZO_ROOT / "scripts" / "summarize_formal_peer_runs.py"


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(PLAN_JSON))
    parser.add_argument("--output-root", default="")
    parser.add_argument("--workflow-ids", default="")
    parser.add_argument("--agents", default="renzo,biomni,stella,tooluniverse")
    parser.add_argument("--baseline-agent", default="renzo")
    parser.add_argument("--renzo-python", default="")
    parser.add_argument("--agent-pythons", default="")
    parser.add_argument("--agent-models", default="")
    parser.add_argument("--parallel-runs", action="store_true")
    parser.add_argument("--strict-agent-manifest", action="store_true")
    parser.add_argument("--max-agent-turns", type=int, default=20)
    parser.add_argument("--timeout-per-step", type=int, default=3600)
    parser.add_argument("--agent-process-timeout", type=int, default=21600)
    parser.add_argument("--require-real-frameworks", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--ignore-env-readiness", action="store_true")
    parser.add_argument("--ignore-evaluability", action="store_true")
    return parser.parse_args()


def load_env_readiness() -> dict[str, dict]:
    if not SANDBOX_STATUS_JSON.exists():
        raise FileNotFoundError(
            f"Sandbox readiness file not found: {SANDBOX_STATUS_JSON}. Run prepare_sandbox_envs.py first."
        )
    payload = json.loads(SANDBOX_STATUS_JSON.read_text(encoding="utf-8"))
    return {row["workflow_id"]: row for row in payload.get("workflow_readiness") or []}


def load_evaluability() -> dict[str, dict]:
    if not EVALUABILITY_STATUS_JSON.exists():
        raise FileNotFoundError(
            f"Workflow evaluability file not found: {EVALUABILITY_STATUS_JSON}. Run check_workflow_evaluability.py first."
        )
    payload = json.loads(EVALUABILITY_STATUS_JSON.read_text(encoding="utf-8"))
    return {row["workflow_id"]: row for row in payload.get("workflow_evaluability") or []}


def main() -> int:
    args = parse_args()
    plan_path = Path(args.plan).resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    rows = list(plan.get("selected_workflows") or [])
    workflow_ids = [item.strip() for item in (args.workflow_ids or "").split(",") if item.strip()]
    if workflow_ids:
        wanted = set(workflow_ids)
        rows = [row for row in rows if row.get("workflow_id") in wanted]
        missing = [wid for wid in workflow_ids if wid not in {row.get("workflow_id") for row in rows}]
        if missing:
            raise SystemExit("Workflow ids not found in plan: " + ", ".join(missing))
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]
    if not args.ignore_env_readiness:
        readiness = load_env_readiness()
        not_ready = [
            row["workflow_id"]
            for row in rows
            if not bool(readiness.get(row["workflow_id"], {}).get("ready"))
        ]
        if not_ready:
            raise SystemExit(
                "Sandbox environments are not ready for: "
                + ", ".join(not_ready)
                + ". Run finish/tools/prepare_sandbox_envs.py first or pass --ignore-env-readiness."
            )
    if not args.ignore_evaluability:
        evaluability = load_evaluability()
        not_evaluable = [
            row["workflow_id"]
            for row in rows
            if not bool(evaluability.get(row["workflow_id"], {}).get("evaluable"))
        ]
        if not_evaluable:
            raise SystemExit(
                "Workflow evaluability gate failed for: "
                + ", ".join(not_evaluable)
                + ". Run finish/tools/check_workflow_evaluability.py first or pass --ignore-evaluability."
            )

    output_root = Path(args.output_root).resolve() if args.output_root else (
        RENZO_ROOT / "data" / "release_runs" / now_tag()
    )
    output_root.mkdir(parents=True, exist_ok=True)

    failures: list[dict[str, str]] = []
    for row in rows:
        workflow_id = row["workflow_id"]
        out_dir = output_root / workflow_id
        cmd = [
            sys.executable,
            str(COMPARISON_SCRIPT),
            "--workflow",
            workflow_id,
            "--output-dir",
            str(out_dir),
            "--agents",
            args.agents,
            "--baseline-agent",
            args.baseline_agent,
            "--timeout-per-step",
            str(args.timeout_per_step),
            "--max-agent-turns",
            str(args.max_agent_turns),
            "--agent-process-timeout",
            str(args.agent_process_timeout),
            *(["--parallel-runs"] if args.parallel_runs else []),
            *(["--strict-agent-manifest"] if args.strict_agent_manifest else []),
            *(["--require-real-frameworks"] if args.require_real_frameworks else []),
            *(["--renzo-python", args.renzo_python] if args.renzo_python else []),
            *(["--agent-pythons", args.agent_pythons] if args.agent_pythons else []),
            *(["--agent-models", args.agent_models] if args.agent_models else []),
        ]
        print(f"[run] {workflow_id}")
        completed = subprocess.run(cmd, cwd=str(ROOT), text=True)
        if completed.returncode != 0:
            failures.append(
                {"workflow_id": workflow_id, "output_dir": str(out_dir), "returncode": str(completed.returncode)}
            )

    if failures:
        fail_path = output_root / "failures.json"
        fail_path.write_text(json.dumps(failures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[warn] failures written to {fail_path}")

    subprocess.run(
        [
            sys.executable,
            str(SUMMARY_SCRIPT),
            "--input-root",
            str(output_root),
        ],
        cwd=str(ROOT),
        check=False,
        text=True,
    )
    print(output_root)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
