from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FINISH_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = FINISH_ROOT.parent
SKILLS_ROOT = REPO_ROOT / ".trae" / "skills"
STATUS_JSON = FINISH_ROOT / "FINISH_EXPANSION_STATUS.json"
REPORT_JSON = FINISH_ROOT / "GENERATED_WORKFLOW_SKILLS.json"
REPORT_MD = FINISH_ROOT / "GENERATED_WORKFLOW_SKILLS.md"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "-", text.lower()).strip("-._")


def title_case(text: str) -> str:
    words = re.split(r"[\s_-]+", text.strip())
    return " ".join(word.capitalize() for word in words if word)


def load_status_rows() -> list[dict]:
    payload = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    return payload.get("rows") or []


def load_manifest(workflow_id: str) -> tuple[Path, dict]:
    workflow_dir = FINISH_ROOT / workflow_id
    manifest_path = workflow_dir / "manifest.json"
    return workflow_dir, json.loads(manifest_path.read_text(encoding="utf-8"))


def existing_skill_specs(workflow_id: str) -> list[Path]:
    root = SKILLS_ROOT / workflow_id
    if not root.exists():
        return []
    return sorted(root.glob("*/SKILL.md"))


def build_reverse_deps(steps: list[dict]) -> dict[str, list[str]]:
    downstream: dict[str, list[str]] = {step["id"]: [] for step in steps}
    for step in steps:
        for dep in step.get("depends_on") or []:
            downstream.setdefault(dep, []).append(step["id"])
    return downstream


def workflow_short_name(workflow_id: str) -> str:
    base = workflow_id[:-7] if workflow_id.endswith("-finish") else workflow_id
    base = base.replace("_", "-")
    return slugify(base)


def describe_step(workflow_name: str, step_id: str, step_name: str, upstream: list[str], downstream: list[str], outputs: list[str]) -> str:
    step_label = step_name or step_id
    upstream_text = f" tied to upstream {', '.join(f'`{x}`' for x in upstream)}" if upstream else ""
    downstream_text = f" and the downstream handoff to {', '.join(f'`{x}`' for x in downstream)}" if downstream else ""
    output_text = ""
    if outputs:
        preview = ", ".join(f"`{x}`" for x in outputs[:3])
        output_text = f" It tracks completion via {preview}."
    return (
        f'Use this skill when orchestrating the retained "{step_id}" step of the {workflow_name} finish workflow.'
        f" It keeps the {step_label} stage{upstream_text}{downstream_text}.{output_text}"
    )


def build_guardrails(step: dict, downstream: list[str]) -> list[str]:
    outputs = step.get("outputs") or []
    params = step.get("params") or {}
    snakefile = params.get("snakefile", "")
    guardrails: list[str] = []
    if any(str(output).endswith(".done") for output in outputs):
        done_files = ", ".join(f"`{x}`" for x in outputs)
        guardrails.append(f"Treat {done_files} as the authoritative completion signal for this wrapped finish step.")
    else:
        guardrails.append("Do not infer completion from narration alone; verify the declared execution outputs exist before handoff.")
    if snakefile:
        guardrails.append(
            f"Keep this stage bounded to `{snakefile}` so the step remains separable and replayable inside the finish workflow."
        )
    if downstream:
        guardrails.append(
            f"Preserve the downstream contract so `{', '.join(downstream)}` can start without recomputing this stage."
        )
    return guardrails[:3]


def build_done_criteria(step_name: str, step: dict, downstream: list[str]) -> str:
    outputs = step.get("outputs") or []
    if outputs:
        target_text = ", ".join(f"`{x}`" for x in outputs[:3])
        if downstream:
            return (
                f"Mark this step complete only when {target_text} exists and "
                f"`{downstream[0]}` can proceed without re-running {step_name or step['id']}."
            )
        return f"Mark this step complete only when {target_text} exists and matches the intended step boundary."
    if downstream:
        return f"Mark this step complete only when the downstream stage `{downstream[0]}` can start from this state directly."
    return "Mark this step complete only when its declared finish boundary is reached and no upstream work must be repeated."


def render_skill(workflow_id: str, workflow_name: str, workflow_dir: Path, step: dict, downstream: list[str]) -> str:
    step_id = step["id"]
    step_name = step.get("name") or title_case(step_id)
    upstream = step.get("depends_on") or []
    params = step.get("params") or {}
    outputs = step.get("outputs") or []
    shared_env = params.get("shared_conda_env", "snakemake")
    step_file = params.get("snakefile", f"steps/{step_id}.smk")
    config_file = params.get("configfile", "config_basic/config.yaml")
    execution_targets = step.get("targets") or outputs
    representative_outputs = outputs or execution_targets

    lines = [
        "---",
        f"name: finish-{workflow_short_name(workflow_id)}-{slugify(step_id)}",
        f"description: {describe_step(workflow_name, step_id, step_name, upstream, downstream, representative_outputs)}",
        "metadata:",
        f"  workflow_id: {workflow_id}",
        f"  workflow_name: {workflow_name}",
        f"  step_id: {step_id}",
        f"  step_name: {step_name}",
        "---",
        "",
        "# Scope",
        f"Use this skill only for the `{step_id}` step in `{workflow_id}`.",
        "",
        "## Orchestration",
        f"- Upstream requirements: {', '.join(f'`{x}`' for x in upstream) if upstream else 'none'}",
        f"- Step file: `finish/{workflow_dir.name}/{step_file}`",
        f"- Config file: `finish/{workflow_dir.name}/{config_file}`",
        f"- Shared environment: `{shared_env}`",
        f"- Completion artifacts: {', '.join(f'`{x}`' for x in outputs) if outputs else 'none declared'}",
        f"- Representative outputs: {', '.join(f'`{x}`' for x in representative_outputs) if representative_outputs else 'none declared'}",
        f"- Execution targets: {', '.join(f'`{x}`' for x in execution_targets) if execution_targets else 'none declared'}",
        f"- Downstream handoff: {', '.join(f'`{x}`' for x in downstream) if downstream else 'none'}",
        "",
        "## Guardrails",
    ]
    for line in build_guardrails(step, downstream):
        lines.append(f"- {line}")
    lines.extend(
        [
            "",
            "## Done Criteria",
            build_done_criteria(step_name, step, downstream),
            "",
        ]
    )
    return "\n".join(lines)


def generate_for_workflow(workflow_id: str, overwrite: bool = False) -> dict:
    workflow_dir, manifest = load_manifest(workflow_id)
    steps = manifest.get("steps") or []
    workflow_name = manifest.get("name") or title_case(workflow_id.replace("-finish", ""))
    downstream = build_reverse_deps(steps)
    workflow_skills_root = SKILLS_ROOT / workflow_id
    workflow_skills_root.mkdir(parents=True, exist_ok=True)

    created = []
    skipped = []
    for step in steps:
        step_id = step["id"]
        skill_dir_name = f"finish-{workflow_short_name(workflow_id)}-{slugify(step_id)}"
        skill_dir = workflow_skills_root / skill_dir_name
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists() and not overwrite:
            skipped.append(step_id)
            continue
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md.write_text(
            render_skill(workflow_id, workflow_name, workflow_dir, step, downstream.get(step_id, [])),
            encoding="utf-8",
        )
        created.append(step_id)
    return {
        "workflow_id": workflow_id,
        "step_count": len(steps),
        "created_count": len(created),
        "skipped_count": len(skipped),
        "created_steps": created,
        "skipped_steps": skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--missing-only", action="store_true", default=True)
    args = parser.parse_args()

    rows = load_status_rows()
    workflow_ids = [row["workflow_id"] for row in rows if str(row.get("workflow_id", "")).endswith("-finish")]
    if args.only:
        wanted = set(args.only)
        workflow_ids = [wid for wid in workflow_ids if wid in wanted]
    results = []
    for workflow_id in sorted(dict.fromkeys(workflow_ids)):
        if args.missing_only and existing_skill_specs(workflow_id):
            continue
        results.append(generate_for_workflow(workflow_id, overwrite=args.overwrite))

    REPORT_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Generated Workflow Skills",
        "",
        f"- Workflows processed: {len(results)}",
        f"- Skills root: `{SKILLS_ROOT}`",
        "",
        "| Workflow | Steps | Created | Skipped |",
        "|---|---:|---:|---:|",
    ]
    for row in results:
        lines.append(
            f"| `{row['workflow_id']}` | {row['step_count']} | {row['created_count']} | {row['skipped_count']} |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(REPORT_JSON)
    print(REPORT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
