from __future__ import annotations

import argparse
import json
import csv
from pathlib import Path
from typing import Any, Dict, List


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_float(value: Any) -> float:
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def safe_int(value: Any) -> int:
    try:
        if value is None or value == "":
            return 0
        return int(value)
    except Exception:
        return 0


def as_json_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def read_optional_json(path_text: str | None) -> Dict[str, Any]:
    if not path_text:
        return {}
    path = Path(path_text).resolve()
    if not path.exists():
        return {}
    return read_json(path)


def flatten_summary(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    workflow_id = str(summary.get("workflow_id") or "")
    baseline = str(summary.get("baseline_agent") or "")
    runs = (summary.get("runs") or {}).get("agents") or {}
    processes = ((summary.get("processes") or {}).get("agents") or {}) if isinstance(summary.get("processes"), dict) else {}
    artifacts = ((summary.get("artifacts") or {}).get("agents") or {}) if isinstance(summary.get("artifacts"), dict) else {}
    rows: List[Dict[str, Any]] = []
    for agent_name, run in runs.items():
        if not isinstance(run, dict):
            continue
        proc = processes.get(agent_name) if isinstance(processes, dict) else None
        raw_run = read_optional_json(artifacts.get(agent_name) if isinstance(artifacts, dict) else None)
        failure_onset = raw_run.get("failure_onset") or {}
        evaluability = raw_run.get("evaluability") or {}
        error_chain = raw_run.get("error_chain") or []
        summary_faithfulness = raw_run.get("summary_faithfulness") or {}
        if run.get("evaluable") is not None:
            evaluable = bool(run.get("evaluable"))
        elif evaluability.get("evaluable") is not None:
            evaluable = bool(evaluability.get("evaluable"))
        else:
            evaluable = True
        recommended_bucket = str(run.get("recommended_bucket") or evaluability.get("recommended_bucket") or ("main_table" if evaluable else ""))
        duration_seconds = None
        started_at = None
        ended_at = None
        if isinstance(proc, dict):
            duration_seconds = proc.get("duration_seconds")
            started_at = proc.get("started_at")
            ended_at = proc.get("ended_at")
        rows.append(
            {
                "workflow_id": workflow_id,
                "agent_name": agent_name,
                "is_baseline": agent_name == baseline,
                "status": str(run.get("status") or ""),
                "workflow_status": str(run.get("workflow_status") or ""),
                "started_at": str(run.get("started_at") or started_at or ""),
                "ended_at": str(run.get("ended_at") or ended_at or ""),
                "duration_seconds": safe_float(run.get("duration_seconds") or duration_seconds or 0.0),
                "step_count": safe_int(run.get("step_count")),
                "completed_step_count": safe_int(run.get("completed_step_count")),
                "turn_count": safe_int(run.get("turn_count")),
                "evaluable": evaluable,
                "recommended_bucket": recommended_bucket,
                "onset_stage": str(run.get("onset_stage") or failure_onset.get("onset_stage") or ""),
                "onset_turn": safe_int(run.get("onset_turn") or failure_onset.get("onset_turn")),
                "onset_step_id": str(run.get("onset_step_id") or failure_onset.get("onset_step_id") or ""),
                "onset_category": str(run.get("onset_category") or failure_onset.get("onset_category") or ""),
                "terminal_symptom": str(run.get("terminal_symptom") or raw_run.get("terminal_symptom") or failure_onset.get("terminal_symptom") or ""),
                "recovery_attempt_count": safe_int(run.get("recovery_attempt_count") or raw_run.get("recovery_attempt_count")),
                "false_success_claim": bool(run.get("false_success_claim")) if run.get("false_success_claim") is not None else bool(raw_run.get("false_success_claim")),
                "trace_node_count": safe_int(run.get("trace_node_count") or ((raw_run.get("trace_tree") or {}).get("node_count"))),
                "trace_stage_count": safe_int(run.get("trace_stage_count") or ((raw_run.get("trace_tree") or {}).get("stage_count"))),
                "time_to_onset": safe_float(failure_onset.get("onset_turn") or 0),
                "error_chain_length": safe_int(len(error_chain)),
                "workflow_noise_flags": as_json_text(run.get("workflow_noise_flags") or raw_run.get("workflow_noise_flags") or []),
                "summary_faithfulness": as_json_text(summary_faithfulness),
                "llm_call_count": safe_int(run.get("llm_call_count")),
                "prompt_tokens": safe_int(run.get("prompt_tokens")),
                "completion_tokens": safe_int(run.get("completion_tokens")),
                "total_tokens": safe_int(run.get("total_tokens")),
                "reasoning_tokens": safe_int(run.get("reasoning_tokens")),
                "cost": safe_float(run.get("cost")),
            }
        )
    return rows


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-csv", default="")
    parser.add_argument("--output-json", default="")
    args = parser.parse_args(argv)

    input_root = Path(args.input_root).resolve()
    if not input_root.exists():
        raise SystemExit(f"input root not found: {input_root}")

    summaries = sorted(input_root.glob("*/artifacts/comparison-summary.json"))
    if not summaries:
        raise SystemExit(f"no comparison-summary.json found under: {input_root}")

    rows: List[Dict[str, Any]] = []
    for path in summaries:
        summary = read_json(path)
        rows.extend(flatten_summary(summary))

    out_json = Path(args.output_json).resolve() if args.output_json else (input_root / "summary_flat.json")
    out_csv = Path(args.output_csv).resolve() if args.output_csv else (input_root / "summary_flat.csv")
    benchmark_json = input_root / "benchmark_main_table.json"
    benchmark_csv = input_root / "benchmark_main_table.csv"
    trace_json = input_root / "trace_audit_table.json"
    trace_csv = input_root / "trace_audit_table.csv"

    out_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    benchmark_rows = [row for row in rows if bool(row.get("evaluable"))]
    trace_rows = list(rows)
    benchmark_json.write_text(json.dumps(benchmark_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    trace_json.write_text(json.dumps(trace_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fieldnames = list(rows[0].keys()) if rows else []
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    with benchmark_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in benchmark_rows:
            writer.writerow(row)
    with trace_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in trace_rows:
            writer.writerow(row)

    print(str(out_csv))
    print(str(out_json))
    print(str(benchmark_csv))
    print(str(benchmark_json))
    print(str(trace_csv))
    print(str(trace_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
