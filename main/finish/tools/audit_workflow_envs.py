from __future__ import annotations

import json
from pathlib import Path


FINISH_ROOT = Path(__file__).resolve().parents[1]
STATUS_JSON = FINISH_ROOT / "FINISH_EXPANSION_STATUS.json"
OUT_JSON = FINISH_ROOT / "WORKFLOW_ENV_AUDIT.json"
OUT_MD = FINISH_ROOT / "WORKFLOW_ENV_AUDIT.md"


SPECIAL_PY2 = {"epigen-300bcg-atacseq_pipeline-finish"}


def load_rows() -> list[dict]:
    payload = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    return payload.get("rows") or []


def env_yaml_count(workflow_id: str) -> int:
    workflow_dir = FINISH_ROOT / workflow_id
    source_meta = workflow_dir / "source-metadata.json"
    if not source_meta.exists():
        return 0
    source_repo = Path(json.loads(source_meta.read_text(encoding="utf-8")).get("source_repo_dir", ""))
    if not source_repo.exists():
        return 0
    return len(list(source_repo.glob("**/envs/*.yaml"))) + len(list(source_repo.glob("**/envs/*.yml")))


def inspect_workflow(workflow_id: str) -> dict:
    workflow_dir = FINISH_ROOT / workflow_id
    manifest = json.loads((workflow_dir / "manifest.json").read_text(encoding="utf-8"))
    config_file = workflow_dir / "config_basic" / "config.yaml"
    config = {}
    if config_file.exists():
        import yaml

        config = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
    steps = manifest.get("steps") or []
    uses_snakemake = any((step.get("params") or {}).get("snakefile") for step in steps)
    command_envs = sorted(
        {
            str(spec.get("command_conda_env") or "").strip()
            for spec in (config.get("steps") or {}).values()
            if str(spec.get("command_conda_env") or "").strip()
        }
        | ({str(config.get("command_conda_env")).strip()} if str(config.get("command_conda_env") or "").strip() else set())
    )
    shared_envs = sorted(
        {
            str((step.get("params") or {}).get("shared_conda_env") or "").strip()
            for step in steps
            if str((step.get("params") or {}).get("shared_conda_env") or "").strip()
        }
    )
    record = {
        "workflow_id": workflow_id,
        "step_count": len(steps),
        "uses_nested_snakemake": uses_snakemake,
        "source_env_yaml_count": env_yaml_count(workflow_id),
        "shared_conda_envs": shared_envs,
        "command_conda_envs": command_envs,
        "needs_python2_isolation": workflow_id in SPECIAL_PY2,
        "notes": [],
    }
    if record["source_env_yaml_count"] > 0:
        record["notes"].append("source workflow ships rule-level conda env YAMLs")
    if command_envs:
        record["notes"].append("manual/special workflow uses dedicated command conda env isolation")
    if workflow_id in SPECIAL_PY2:
        record["notes"].append("requires Python 2 isolation due to legacy pypiper/StringIO stack")
    return record


def main() -> int:
    rows = [row for row in load_rows() if str(row.get("workflow_id", "")).endswith("-finish")]
    records = [inspect_workflow(row["workflow_id"]) for row in rows]
    OUT_JSON.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Workflow Environment Audit",
        "",
        "更新日期: 2026-04-10",
        "",
        f"- 审计 workflow 数: {len(records)}",
        "",
        "| Workflow | Steps | Nested Snakemake | Source env yaml | Shared env | Command env |",
        "|---|---:|---|---:|---|---|",
    ]
    for row in records:
        lines.append(
            f"| `{row['workflow_id']}` | {row['step_count']} | {row['uses_nested_snakemake']} | "
            f"{row['source_env_yaml_count']} | {', '.join(row['shared_conda_envs']) or '-'} | "
            f"{', '.join(row['command_conda_envs']) or '-'} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_JSON)
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
