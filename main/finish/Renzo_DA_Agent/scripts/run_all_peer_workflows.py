from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FINISH_ROOT = ROOT.parent


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def discover_workflow_ids() -> list[str]:
    ids: list[str] = []
    for manifest_path in FINISH_ROOT.glob("*/manifest.json"):
        if manifest_path.parent.name == "Renzo_DA_Agent":
            continue
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        workflow_id = str(payload.get("id") or "").strip()
        if workflow_id:
            ids.append(workflow_id)
    return sorted(list(dict.fromkeys(ids)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", default="")
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
    args = parser.parse_args(argv)

    workflow_ids = discover_workflow_ids()
    if not workflow_ids:
        print("No workflows found under finish/*/manifest.json", file=sys.stderr)
        return 2

    output_root = Path(args.output_root).resolve() if args.output_root else (ROOT / "data" / "formal_peer_runs" / now_tag())
    output_root.mkdir(parents=True, exist_ok=True)

    script = ROOT / "scripts" / "run_finish_workflow_comparison.py"
    if not script.exists():
        print(f"Missing script: {script}", file=sys.stderr)
        return 2

    failures: list[dict[str, str]] = []
    for wid in workflow_ids:
        out_dir = output_root / wid
        cmd = [
            sys.executable,
            str(script),
            "--workflow",
            wid,
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
        print(f"[run] workflow={wid} -> {out_dir}")
        completed = subprocess.run(cmd, text=True)
        if completed.returncode != 0:
            failures.append({"workflow_id": wid, "output_dir": str(out_dir), "returncode": str(completed.returncode)})

    if failures:
        fail_path = output_root / "failures.json"
        fail_path.write_text(json.dumps(failures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[done] failures recorded: {fail_path}")
        return 1

    print(f"[done] all workflows finished: {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
