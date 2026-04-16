from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_workflows() -> dict[str, dict[str, object]]:
    workflows: dict[str, dict[str, object]] = {}
    for manifest_path in sorted(ROOT.glob("*/manifest.json")):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        steps = [str(step.get("id")) for step in data.get("steps", []) if step.get("id")]
        if not steps:
            continue
        workflow_dir = manifest_path.parent
        aliases = [
            str(alias)
            for alias in (
                data.get("aliases")
                or (data.get("discovery", {}) or {}).get("aliases")
                or []
            )
            if str(alias).strip()
        ]
        record = {
            "id": str(data.get("id", workflow_dir.name)),
            "name": str(data.get("name", workflow_dir.name)),
            "dir": workflow_dir,
            "steps": steps,
            "aliases": aliases,
        }
        keys = [record["id"], workflow_dir.name, *aliases]
        for key in keys:
            workflows[str(key)] = record
    return workflows


def parse_args() -> argparse.Namespace:
    workflow_choices = sorted(load_workflows())
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", choices=workflow_choices, required=True)
    parser.add_argument("--cores", default="8")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-step")
    parser.add_argument("--to-step")
    return parser.parse_args()


def build_command(step_id: str, cores: str, dry_run: bool) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "snakemake",
        "-s",
        f"steps/{step_id}.smk",
        "--configfile",
        "config_basic/config.yaml",
        "--cores",
        cores,
    ]
    if dry_run:
        command.append("-n")
    return command


def selected_steps(all_steps: list[str], start: str | None, end: str | None) -> list[str]:
    start_index = all_steps.index(start) if start else 0
    end_index = all_steps.index(end) + 1 if end else len(all_steps)
    if start_index >= end_index:
        raise ValueError("from-step 必须早于或等于 to-step")
    return all_steps[start_index:end_index]


def main() -> int:
    args = parse_args()
    workflows = load_workflows()
    workflow = workflows[args.workflow]
    steps = selected_steps(workflow["steps"], args.from_step, args.to_step)
    for step_id in steps:
        command = build_command(step_id, args.cores, args.dry_run)
        print(f"== {workflow['id']}:{step_id} ==")
        print(" ".join(command))
        proc = subprocess.run(command, cwd=workflow["dir"])
        if proc.returncode != 0:
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
