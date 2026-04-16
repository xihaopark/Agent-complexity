from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLAN_JSON = ROOT / "BENCHMARK_RUN_PLAN.json"
SANDBOX_STATUS_JSON = ROOT / "SANDBOX_ENV_STATUS.json"
OUTPUT_JSON = ROOT / "WORKFLOW_EVALUABILITY_STATUS.json"
OUTPUT_MD = ROOT / "WORKFLOW_EVALUABILITY_STATUS.md"

KNOWN_SMOKE_BLOCKERS: dict[str, dict[str, str]] = {
    "rna-seq-star-deseq2-finish": {
        "category": "input_or_env_failure",
        "reason": "Known smoke blocker: staged FASTQ inputs are incomplete in the current finish context.",
        "bucket": "fix_then_retry",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default=str(PLAN_JSON))
    parser.add_argument("--workflows", default="")
    parser.add_argument("--output-json", default=str(OUTPUT_JSON))
    parser.add_argument("--output-md", default=str(OUTPUT_MD))
    return parser.parse_args()


def load_target_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.workflows.strip():
        rows = []
        for workflow_id in [item.strip() for item in args.workflows.split(",") if item.strip()]:
            workflow_dir = ROOT / workflow_id
            rows.append({"workflow_id": workflow_id, "workflow_dir": str(workflow_dir)})
        return rows
    plan = read_json(Path(args.plan).resolve())
    return list(plan.get("selected_workflows") or [])


def load_env_readiness() -> dict[str, dict[str, Any]]:
    if not SANDBOX_STATUS_JSON.exists():
        return {}
    payload = read_json(SANDBOX_STATUS_JSON)
    return {str(row["workflow_id"]): row for row in payload.get("workflow_readiness") or []}


def parse_yaml(path: Path) -> dict[str, Any]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def manifest_protocol_checks(workflow_dir: Path, manifest: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    reasons: list[str] = []
    evidence: list[str] = []
    steps = manifest.get("steps") or []
    if not steps:
        reasons.append("manifest has no steps")
        evidence.append("manifest.steps is empty")
        return False, reasons, evidence

    step_ids: list[str] = []
    seen: set[str] = set()
    for index, step in enumerate(steps, start=1):
        step_id = str(step.get("id") or "").strip()
        if not step_id:
            reasons.append(f"step {index} is missing id")
            continue
        if step_id in seen:
            reasons.append(f"duplicate step id: {step_id}")
        seen.add(step_id)
        step_ids.append(step_id)
        snakefile = workflow_dir / str((step.get("params") or {}).get("snakefile") or f"steps/{step_id}.smk")
        if not snakefile.exists():
            reasons.append(f"missing snakefile for step {step_id}")
            evidence.append(str(snakefile))
        configfile = (step.get("params") or {}).get("configfile")
        if configfile:
            config_path = workflow_dir / str(configfile)
            if not config_path.exists():
                reasons.append(f"missing configfile for step {step_id}")
                evidence.append(str(config_path))
    known_ids = set(step_ids)
    for step in steps:
        step_id = str(step.get("id") or "")
        for dep in step.get("depends_on") or []:
            dep_id = str(dep)
            if dep_id not in known_ids:
                reasons.append(f"step {step_id} depends on unknown step {dep_id}")
    return not reasons, reasons, evidence


def input_readiness_checks(workflow_dir: Path, manifest: dict[str, Any], config_payload: dict[str, Any]) -> tuple[bool, list[str], list[str]]:
    reasons: list[str] = []
    evidence: list[str] = []

    input_hints = [str(item) for item in manifest.get("input_hints") or [] if str(item).strip()]
    if input_hints:
        resolved_hints = [(workflow_dir / hint).resolve() for hint in input_hints]
        existing_hints = [path for path in resolved_hints if path.exists()]
        if not existing_hints:
            reasons.append("none of the manifest input_hints currently exist")
            evidence.extend(str(path) for path in resolved_hints[:5])

    steps_cfg = config_payload.get("steps") or {}
    missing_requires: list[str] = []
    for step_id, step_cfg in steps_cfg.items():
        if not isinstance(step_cfg, dict):
            continue
        for req in step_cfg.get("requires") or []:
            req_path = Path(str(req))
            resolved = req_path if req_path.is_absolute() else (workflow_dir / str(req)).resolve()
            if not resolved.exists():
                missing_requires.append(f"{step_id}:{resolved}")
    if missing_requires:
        reasons.append("missing required input paths declared in config_basic/config.yaml")
        evidence.extend(missing_requires[:10])

    return not reasons, reasons, evidence


def evaluate_workflow(row: dict[str, Any], env_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    workflow_id = str(row.get("workflow_id") or "")
    workflow_dir = Path(str(row.get("workflow_dir") or (ROOT / workflow_id))).resolve()
    manifest_path = workflow_dir / "manifest.json"
    env_row = env_rows.get(workflow_id) or {}

    protocol_ok = False
    inputs_ready = False
    env_ready = bool(env_row.get("ready"))
    reasons: list[str] = []
    evidence: list[str] = []
    noise_flags: list[str] = []
    bucket = "main_table"

    if not manifest_path.exists():
        reasons.append("manifest.json missing")
        evidence.append(str(manifest_path))
    else:
        manifest = read_json(manifest_path)
        config_path = workflow_dir / "config_basic" / "config.yaml"
        config_payload = parse_yaml(config_path) if config_path.exists() else {}
        protocol_ok, protocol_reasons, protocol_evidence = manifest_protocol_checks(workflow_dir, manifest)
        reasons.extend(protocol_reasons)
        evidence.extend(protocol_evidence)
        inputs_ready, input_reasons, input_evidence = input_readiness_checks(workflow_dir, manifest, config_payload)
        reasons.extend(input_reasons)
        evidence.extend(input_evidence)

    if workflow_id in KNOWN_SMOKE_BLOCKERS:
        blocker = KNOWN_SMOKE_BLOCKERS[workflow_id]
        reasons.append(blocker["reason"])
        noise_flags.append(blocker["category"])
        bucket = blocker["bucket"]

    if not env_ready:
        reasons.append(f"env readiness is false: {env_row.get('detail') or 'missing sandbox readiness'}")
        if env_row:
            evidence.append(str(env_row.get("detail") or ""))
        noise_flags.append("input_or_env_failure")
        if bucket == "main_table":
            bucket = "fix_then_retry"

    evaluable = bool(protocol_ok and inputs_ready and env_ready and workflow_id not in KNOWN_SMOKE_BLOCKERS)
    if not protocol_ok:
        noise_flags.append("workflow_protocol_failure")
        if bucket == "main_table":
            bucket = "fix_then_retry"
    if not inputs_ready:
        noise_flags.append("input_or_env_failure")
        if bucket == "main_table":
            bucket = "fix_then_retry"

    if evaluable:
        reasons = ["workflow is evaluable under current manifest/input/env checks"]
        noise_flags = []
        bucket = "main_table"

    return {
        "workflow_id": workflow_id,
        "workflow_dir": str(workflow_dir),
        "evaluable": evaluable,
        "protocol_ok": protocol_ok,
        "inputs_ready": inputs_ready,
        "env_ready": env_ready,
        "reason": reasons[0] if reasons else "",
        "evidence": [item for item in evidence if item][:10],
        "noise_flags": sorted(dict.fromkeys(noise_flags)),
        "recommended_bucket": bucket,
    }


def write_md(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Workflow Evaluability Status",
        "",
        f"- 生成时间: {Path(__file__).resolve()}",
        f"- 总数: {len(rows)}",
        f"- Evaluable: {sum(1 for row in rows if row['evaluable'])}",
        "",
        "| Workflow | Evaluable | Protocol | Inputs | Env | Bucket | Reason |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['workflow_id']}` | {row['evaluable']} | {row['protocol_ok']} | "
            f"{row['inputs_ready']} | {row['env_ready']} | {row['recommended_bucket']} | "
            f"{str(row['reason']).replace('|', '/')} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows = load_target_rows(args)
    env_rows = load_env_readiness()
    output_rows = [evaluate_workflow(row, env_rows) for row in rows]
    payload = {
        "generated_at": Path(__file__).resolve().as_posix(),
        "summary": {
            "total": len(output_rows),
            "evaluable_count": sum(1 for row in output_rows if row["evaluable"]),
            "not_evaluable_count": sum(1 for row in output_rows if not row["evaluable"]),
        },
        "workflow_evaluability": output_rows,
    }
    out_json = Path(args.output_json).resolve()
    out_md = Path(args.output_md).resolve()
    write_json(out_json, payload)
    write_md(out_md, output_rows)
    print(out_json)
    print(out_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
