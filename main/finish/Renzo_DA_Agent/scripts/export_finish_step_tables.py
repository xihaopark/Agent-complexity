#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMPARISONS_DIR = ROOT / "data" / "finish_run_comparisons"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "reports" / "step_tables"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in text).strip("-_") or "workflow"


def latest_runs_by_workflow(comparisons_dir: Path) -> dict[str, Path]:
    latest: dict[str, Path] = {}
    for run_dir in sorted((p for p in comparisons_dir.iterdir() if p.is_dir()), key=lambda p: p.name):
        artifacts = run_dir / "artifacts"
        agent_json = artifacts / "agent-run.json"
        direct_json = artifacts / "direct-run.json"
        if not agent_json.exists() or not direct_json.exists():
            continue
        try:
            workflow_id = load_json(agent_json).get("workflow_id") or load_json(direct_json).get("workflow_id")
        except Exception:
            continue
        if workflow_id:
            latest[workflow_id] = run_dir
    return latest


def metrics_by_step(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item.get("step_id")): item for item in items if item.get("step_id")}


def compact(text: str, limit: int = 180) -> str:
    clean = " ".join(str(text or "").split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 1] + "…"


def step_rows(run_dir: Path) -> tuple[str, list[dict[str, Any]]]:
    artifacts = run_dir / "artifacts"
    agent = load_json(artifacts / "agent-run.json")
    direct = load_json(artifacts / "direct-run.json")
    workflow_id = str(agent.get("workflow_id") or direct.get("workflow_id") or run_dir.name)

    agent_steps = metrics_by_step(agent.get("step_metrics") or [])
    direct_steps = metrics_by_step(direct.get("step_metrics") or [])
    step_ids = sorted(
        set(agent_steps) | set(direct_steps),
        key=lambda step_id: (
            (agent_steps.get(step_id) or direct_steps.get(step_id) or {}).get("declared_order", 10**9),
            step_id,
        ),
    )

    rows: list[dict[str, Any]] = []
    for step_id in step_ids:
        a = agent_steps.get(step_id, {})
        d = direct_steps.get(step_id, {})
        agent_exec_status = str(a.get("execution_status", "") or "")
        if agent_exec_status in {"", "not_run"}:
            if a.get("plan_status") == "success":
                agent_exec_status = "success"
            elif a.get("plan_status") == "failed":
                agent_exec_status = "failed"
        rows.append(
            {
                "workflow_id": workflow_id,
                "step_order": a.get("declared_order", d.get("declared_order", "")),
                "step_id": step_id,
                "step_name": a.get("step_name", d.get("step_name", "")),
                "direct_status": d.get("execution_status", ""),
                "direct_attempts": d.get("execution_attempt_count", ""),
                "direct_seconds": d.get("duration_seconds_total", ""),
                "agent_plan_status": a.get("plan_status", ""),
                "agent_exec_status": agent_exec_status,
                "agent_turns": a.get("turn_count", ""),
                "agent_attempts": a.get("execution_attempt_count", ""),
                "agent_seconds": a.get("duration_seconds_total", ""),
                "llm_calls": a.get("llm_call_count", 0),
                "prompt_tokens": a.get("prompt_tokens", 0),
                "completion_tokens": a.get("completion_tokens", 0),
                "total_tokens": a.get("total_tokens", 0),
                "reasoning_tokens": a.get("reasoning_tokens", 0),
                "cost_usd": a.get("cost", 0.0),
                "selection_reason": compact(a.get("last_selection_reason", "")),
                "llm_excerpt": compact(a.get("latest_llm_response_excerpt", "")),
            }
        )
    return workflow_id, rows


def markdown_table(rows: list[dict[str, Any]], *, workflow_id: str, run_dir: Path, agent: dict[str, Any], direct: dict[str, Any]) -> str:
    usage = agent.get("llm_usage_summary") or {}
    summary_lines = [
        f"Workflow: `{workflow_id}`",
        f"Run: `{run_dir.name}`",
        f"Direct status: `{direct.get('status', '')}`",
        f"Agent status: `{agent.get('status', '')}`",
        f"Agent turns: `{agent.get('turn_count', 0)}`",
        f"LLM calls: `{usage.get('llm_call_count', 0)}`",
        f"Total tokens: `{usage.get('total_tokens', 0)}`",
        f"Prompt tokens: `{usage.get('prompt_tokens', 0)}`",
        f"Completion tokens: `{usage.get('completion_tokens', 0)}`",
        f"Reasoning tokens: `{usage.get('reasoning_tokens', 0)}`",
        f"Total cost (USD): `{usage.get('cost', 0.0)}`",
        "",
    ]
    headers = [
        "Step",
        "Direct",
        "Direct(s)",
        "Agent Plan",
        "Agent Exec",
        "Turns",
        "LLM Calls",
        "Tokens",
        "Cost(USD)",
        "Reason / Trace",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        reason = row["selection_reason"] or row["llm_excerpt"]
        lines.append(
            "| {step} | {direct} | {dsec} | {aplan} | {aexec} | {turns} | {calls} | {tokens} | {cost} | {reason} |".format(
                step=f"{row['step_order']}. {row['step_id']}",
                direct=row["direct_status"] or "-",
                dsec=row["direct_seconds"] if row["direct_seconds"] != "" else "-",
                aplan=row["agent_plan_status"] or "-",
                aexec=row["agent_exec_status"] or "-",
                turns=row["agent_turns"] if row["agent_turns"] != "" else "-",
                calls=row["llm_calls"],
                tokens=row["total_tokens"],
                cost=("{:.6f}".format(float(row["cost_usd"]))).rstrip("0").rstrip(".") if row["cost_usd"] not in ("", None) else "-",
                reason=(reason or "-").replace("|", "/"),
            )
        )
    return "\n".join(summary_lines + lines) + "\n"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export finish workflow step tables for PPT/reporting.")
    parser.add_argument("--comparisons-dir", default=str(DEFAULT_COMPARISONS_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--workflow", action="append", help="Specific workflow_id to export. Can be repeated.")
    parser.add_argument("--require-success", action="store_true", help="Only export runs where both direct and agent succeeded.")
    args = parser.parse_args()

    comparisons_dir = Path(args.comparisons_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    selected = set(args.workflow or [])
    run_map = latest_runs_by_workflow(comparisons_dir)

    exported: list[str] = []
    for workflow_id, run_dir in sorted(run_map.items()):
        if selected and workflow_id not in selected:
            continue
        agent = load_json(run_dir / "artifacts" / "agent-run.json")
        direct = load_json(run_dir / "artifacts" / "direct-run.json")
        if args.require_success and (agent.get("status") != "success" or direct.get("status") != "success"):
            continue
        _, rows = step_rows(run_dir)
        stem = slugify(workflow_id)
        write_csv(output_dir / f"{stem}.csv", rows)
        (output_dir / f"{stem}.md").write_text(
            markdown_table(rows, workflow_id=workflow_id, run_dir=run_dir, agent=agent, direct=direct),
            encoding="utf-8",
        )
        exported.append(f"{workflow_id}\t{run_dir.name}")

    (output_dir / "index.tsv").write_text("\n".join(exported) + ("\n" if exported else ""), encoding="utf-8")
    print(f"Exported {len(exported)} workflow step tables to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
