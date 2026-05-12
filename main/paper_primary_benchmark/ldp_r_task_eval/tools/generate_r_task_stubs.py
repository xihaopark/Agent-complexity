#!/usr/bin/env python3
"""Generate R-task evaluation stubs from task_definitions (145 stages) + merge pilot_hello into registry."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# paper_primary_benchmark / ldp_r_task_eval / tools / this file
_LDP_EVAL = Path(__file__).resolve().parent.parent
_PAPER_PB = _LDP_EVAL.parent
_TASK_DEF = _PAPER_PB / "task_definitions"
_MANIFEST = _PAPER_PB / "manifest.json"
_STUB_ROOT = _LDP_EVAL / "tasks" / "stubs"
_REGISTRY_DIR = _LDP_EVAL / "r_tasks"
_REGISTRY_PATH = _REGISTRY_DIR / "registry.json"

PILOT_ENTRY = {
    "id": "pilot_hello",
    "work_dir": "ldp_r_task_eval/tasks/pilot_hello",
    "success_artifact_glob": "output/result.txt",
    "status": "ready",
    "pipeline_workflow_id": None,
    "pipeline_task_id": None,
    "family": None,
}


def _load_manifest_families() -> dict[str, str]:
    if not _MANIFEST.is_file():
        return {}
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for w in data.get("main_workflows", []):
        wid = w.get("id")
        fam = w.get("family")
        if wid and fam:
            out[wid] = fam
    return out


def _io_lines(items: list[dict], label: str) -> list[str]:
    lines: list[str] = [f"### {label}"]
    if not items:
        lines.append("_(none listed in task_definitions)_")
        return lines
    for it in items:
        parts = []
        if it.get("role"):
            parts.append(f"**{it['role']}**")
        if it.get("path_glob"):
            parts.append(f"`{it['path_glob']}`")
        if it.get("description"):
            parts.append(it["description"])
        if it.get("derived_from_step_ids"):
            parts.append(f"(from steps: {', '.join(it['derived_from_step_ids'])})")
        lines.append("- " + " — ".join(parts) if parts else "- _(empty item)_")
    return lines


def _write_objective(
    path: Path,
    *,
    workflow_id: str,
    task: dict,
    manifest_path: str,
) -> None:
    label = task.get("pipeline_stage_label", "")
    summary = (task.get("metadata") or {}).get("summary", "")
    step_ids = task.get("step_ids", [])
    tid = task["task_id"]
    order = task.get("order", 0)
    steps_md = "\n".join(f"- `{s}`" for s in step_ids) or "- _(none)_"
    inputs_md = "\n".join(_io_lines(task.get("inputs") or [], "Declared inputs (path hints)"))
    outputs_md = "\n".join(_io_lines(task.get("outputs") or [], "Declared outputs (path hints)"))

    body = f"""# R-task stub: `{workflow_id}` / `{tid}`

> **Status:** stub — evaluation inputs, metrics, and gold outputs are **not** filled in yet.
> Pipeline overlay comes from `paper_primary_benchmark/task_definitions/{workflow_id}.json`.

## Stage

- **Label:** {label}
- **Order:** {order}
- **Finish manifest (reference):** `{manifest_path}`

## Snakemake steps in this stage

{steps_md}

## Summary (from task_definitions metadata)

{summary or "_No metadata.summary._"}

{inputs_md}

{outputs_md}

## TODO — fill before marking `status: ready` in registry

1. **Data:** Place minimal inputs under `input/` (or document symlinks/capsules). Do not commit large raw data without LFS or external URLs.
2. **Objective:** Replace this stub text with precise success criteria (files, metrics, thresholds).
3. **Gold / baseline:** Optional path to expected artifacts or a Snakemake/finish command used to produce reference outputs.
4. **Environment:** Note R/Bioconductor/conda requirements if different from the default pilot.

## Default env hint

`RTaskEvalEnv` expects a success artifact (see registry `success_artifact_glob`, default `output/result.txt`) before `submit_done(success=true)` with reward.
"""
    path.write_text(body.strip() + "\n", encoding="utf-8")


def _write_meta(
    path: Path,
    *,
    workflow_id: str,
    task: dict,
    manifest_path: str,
) -> None:
    meta = {
        "workflow_id": workflow_id,
        "pipeline_task_id": task["task_id"],
        "order": task.get("order"),
        "manifest_path": manifest_path,
        "step_ids": task.get("step_ids", []),
        "status": "stub",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _stub_dir_name(workflow_id: str, task_id: str) -> str:
    return f"{workflow_id}__{task_id}"


def generate(
    *,
    dry_run: bool,
    force: bool,
) -> tuple[int, int, int, list[dict]]:
    """Returns (new_dirs, skipped_existing_no_force, rewritten_force, registry_tasks)."""
    families = _load_manifest_families()
    registry_tasks: list[dict] = [dict(PILOT_ENTRY)]

    new_dirs = 0
    skipped_existing = 0
    rewritten = 0

    defs = sorted(_TASK_DEF.glob("*.json"))
    for fp in defs:
        if fp.name == "schema.json":
            continue
        data = json.loads(fp.read_text(encoding="utf-8"))
        workflow_id = data["workflow_id"]
        manifest_path = data.get("manifest_path", "")
        family = families.get(workflow_id)

        for task in data.get("tasks", []):
            tid = task["task_id"]
            dirname = _stub_dir_name(workflow_id, tid)
            stub_path = _STUB_ROOT / dirname
            rel_work = f"ldp_r_task_eval/tasks/stubs/{dirname}"
            entry = {
                "id": dirname,
                "work_dir": rel_work,
                "success_artifact_glob": "output/result.txt",
                "status": "stub",
                "pipeline_workflow_id": workflow_id,
                "pipeline_task_id": tid,
                "family": family,
            }
            registry_tasks.append(entry)

            if dry_run:
                print(f"would create or update: {stub_path}")
                continue

            exists = stub_path.is_dir()
            if exists and not force:
                skipped_existing += 1
                continue

            if not exists:
                stub_path.mkdir(parents=True, exist_ok=True)
                (stub_path / "input").mkdir(exist_ok=True)
                (stub_path / "output").mkdir(exist_ok=True)
                for sub in ("input", "output"):
                    gk = stub_path / sub / ".gitkeep"
                    if not gk.exists():
                        gk.write_text("", encoding="utf-8")
                new_dirs += 1

            _write_objective(
                stub_path / "OBJECTIVE.md",
                workflow_id=workflow_id,
                task=task,
                manifest_path=manifest_path,
            )
            _write_meta(
                stub_path / "meta.json",
                workflow_id=workflow_id,
                task=task,
                manifest_path=manifest_path,
            )
            if exists and force:
                rewritten += 1

    if dry_run:
        n = len(registry_tasks) - 1  # exclude pilot for stub count
        print(f"dry-run: {n} pipeline stubs + pilot; registry would have {len(registry_tasks)} tasks")
        return 0, 0, 0, registry_tasks

    _REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    registry_obj = {
        "version": 2,
        "description": (
            "R-task registry: pilot_hello (ready) + 145 pipeline-stage stubs. "
            "Paths relative to paper_primary_benchmark/."
        ),
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "task_definitions_note": (
            "Stubs generated from paper_primary_benchmark/task_definitions/*.json; "
            "see each stub OBJECTIVE.md and meta.json."
        ),
        "tasks": registry_tasks,
    }
    _REGISTRY_PATH.write_text(
        json.dumps(registry_obj, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return new_dirs, skipped_existing, rewritten, registry_tasks


def main() -> None:
    p = argparse.ArgumentParser(
        description="Generate ldp_r_task_eval stubs from task_definitions and write r_tasks/registry.json"
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths only; do not write files",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help=(
            "Rewrite OBJECTIVE.md and meta.json even if stub dirs exist. "
            "WARNING: destroys sample_50-prepared workspaces and any hand-edited stubs."
        ),
    )
    args = p.parse_args()

    if not _TASK_DEF.is_dir():
        print("ERROR: task_definitions not found:", _TASK_DEF, file=sys.stderr)
        sys.exit(1)

    new_dirs, skipped, rew, tasks = generate(dry_run=args.dry_run, force=args.force)
    if not args.dry_run:
        print(f"Wrote registry with {len(tasks)} tasks -> {_REGISTRY_PATH}")
        print(f"New stub directories created: {new_dirs}")
        if skipped:
            print(f"Skipped existing stubs (no --force): {skipped}")
        if rew:
            print(f"Rewrote OBJECTIVE/meta (--force): {rew}")


if __name__ == "__main__":
    main()
