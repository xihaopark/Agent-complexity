from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_JSON = ROOT / "BENCHMARK_RELEASE_CANDIDATES.json"
RUNNER = ROOT / "run_finish_workflow.py"
OUT_JSON = ROOT / "SMOKE_TEST_RESULTS.json"
OUT_MD = ROOT / "SMOKE_TEST_RESULTS.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", choices=["core", "extended", "large", "all"], default="core")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--cores", default="1")
    parser.add_argument("--no-dry-run", action="store_true")
    parser.add_argument("--only", nargs="*")
    return parser.parse_args()


def load_workflows(args: argparse.Namespace) -> list[dict]:
    data = json.loads(RELEASE_JSON.read_text(encoding="utf-8"))
    rows = []
    if args.tier in {"core", "all"}:
        rows.extend(data.get("release_core") or [])
    if args.tier in {"extended", "all"}:
        rows.extend(data.get("release_extended") or [])
    if args.tier in {"large", "all"}:
        rows.extend(data.get("release_large") or [])
    if args.only:
        only = set(args.only)
        rows = [row for row in rows if row.get("workflow_id") in only]
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]
    return rows


def run_one(workflow_id: str, cores: str, dry_run: bool) -> dict:
    command = [sys.executable, str(RUNNER), "--workflow", workflow_id, "--cores", cores]
    if dry_run:
        command.append("--dry-run")
    started = time.time()
    completed = subprocess.run(
        command,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "workflow_id": workflow_id,
        "started_at": datetime.fromtimestamp(started, tz=timezone.utc).isoformat(),
        "ended_at": now_iso(),
        "duration_seconds": round(time.time() - started, 3),
        "returncode": completed.returncode,
        "status": "passed" if completed.returncode == 0 else "failed",
        "command": command,
        "stdout_tail": "\n".join(completed.stdout.splitlines()[-30:]),
        "stderr_tail": "\n".join(completed.stderr.splitlines()[-30:]),
    }


def write_reports(results: list[dict], dry_run: bool) -> None:
    payload = {
        "mode": "dry-run" if dry_run else "real-run",
        "count": len(results),
        "passed": sum(1 for row in results if row["status"] == "passed"),
        "failed": sum(1 for row in results if row["status"] == "failed"),
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Smoke Test Results",
        "",
        f"- 模式: {'dry-run' if dry_run else 'real-run'}",
        f"- 总数: {payload['count']}",
        f"- 通过: {payload['passed']}",
        f"- 失败: {payload['failed']}",
        "",
        "| Workflow | Status | Duration(s) |",
        "|---|---|---:|",
    ]
    for row in results:
        lines.append(f"| `{row['workflow_id']}` | {row['status']} | {row['duration_seconds']} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    dry_run = not args.no_dry_run
    rows = load_workflows(args)
    results = [run_one(row["workflow_id"], args.cores, dry_run) for row in rows]
    write_reports(results, dry_run=dry_run)
    print(OUT_JSON)
    print(OUT_MD)
    return 0 if all(row["status"] == "passed" for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
