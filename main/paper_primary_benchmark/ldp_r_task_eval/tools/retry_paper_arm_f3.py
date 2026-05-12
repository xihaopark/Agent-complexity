#!/usr/bin/env python3
"""Retry specific tasks for the paper arm sweep (F3 finish protocol).

This script runs specific missing tasks from a paper arm batch sweep,
using the same configuration as the original sweep.

Usage:
    python retry_paper_arm_f3.py --tasks 9,10,11 --batch-id sweep_v3_paper_20260416T194356Z
    python retry_paper_arm_f3.py --task-range 9,31 --batch-id sweep_v3_paper_20260416T194356Z
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

# Add repo to path
_PAPER_PB = Path(__file__).resolve().parent.parent
_MAIN = _PAPER_PB.parent
_REPO_ROOT = _MAIN.parent
if str(_MAIN) not in sys.path:
    sys.path.insert(0, str(_MAIN))

from paper_primary_benchmark.ldp_r_task_eval.batch_runner import (
    _one_task,
    _load_registry,
    _load_yaml,
    _SKILL_SOURCES,
    _DEFAULT_MANIFEST_BY_SOURCE,
    _load_skill_manifest,
)
from paper_primary_benchmark.ldp_r_task_eval.llm_env import apply_openrouter_key_from_file

logger = logging.getLogger(__name__)


def parse_task_indices(tasks_str: str | None, task_range_str: str | None) -> list[int]:
    """Parse task indices from --tasks or --task-range."""
    indices = []
    if tasks_str:
        for part in tasks_str.split(","):
            indices.append(int(part.strip()))
    elif task_range_str:
        start, end = task_range_str.split(",")
        indices = list(range(int(start.strip()), int(end.strip()) + 1))
    return indices


async def main_async(args: argparse.Namespace) -> int:
    cfg = _load_yaml(Path(args.config).resolve())

    # Set up API key
    key_path = Path(args.openrouter_key_file).resolve()
    # Read line 2 explicitly if requested
    if args.key_line == 2 and key_path.is_file():
        lines = key_path.read_text(encoding="utf-8").splitlines()
        non_empty = [l.strip() for l in lines if l.strip()]
        if len(non_empty) >= 2:
            os.environ["OPENROUTER_API_KEY"] = non_empty[1]
            logger.info("Set OPENROUTER_API_KEY from line 2 of %s", key_path)
        else:
            logger.error("Key file has fewer than 2 non-empty lines")
            return 2
    elif apply_openrouter_key_from_file(key_path):
        logger.info("Set OPENROUTER_API_KEY from %s (line 1)", key_path)
    elif not os.environ.get("OPENROUTER_API_KEY"):
        logger.error("No OpenRouter key available")
        return 2

    # Load registry
    reg = _load_registry(Path(args.registry).resolve())
    tasks = reg.get("tasks", [])

    # Parse task indices
    indices = parse_task_indices(args.tasks, args.task_range)
    if not indices:
        logger.error("No tasks specified. Use --tasks or --task-range")
        return 2

    # Validate indices
    for idx in indices:
        if idx < 0 or idx >= len(tasks):
            logger.error("Task index %d out of range (0-%d)", idx, len(tasks) - 1)
            return 2

    logger.info("Will run %d tasks: indices %s", len(indices), indices)
    logger.info("Batch ID: %s", args.batch_id)
    logger.info("Skill source: %s", args.skill_source)

    # Load skill manifest for paper arm
    skill_manifest = None
    if args.skill_source != "none":
        if args.skill_manifest:
            manifest_path = Path(args.skill_manifest).resolve()
        else:
            manifest_path = _DEFAULT_MANIFEST_BY_SOURCE[args.skill_source].resolve()
        if not manifest_path.is_file():
            logger.error("Skill manifest not found: %s", manifest_path)
            return 2
        skill_manifest = _load_skill_manifest(manifest_path)
        logger.info("Loaded skill manifest: %s", manifest_path)

    # Override config settings
    cfg["max_steps"] = args.max_steps
    if "agent" not in cfg:
        cfg["agent"] = {}
    cfg["agent"]["llm_model"] = {
        "name": args.model,
        "temperature": args.temperature,
    }

    failed: list[tuple[int, str, str]] = []
    completed = 0

    for idx in indices:
        entry = tasks[idx]
        task_id = entry["id"]
        try:
            logger.info("Starting task %d: %s", idx, task_id)
            await _one_task(
                entry,
                cfg=cfg,
                smoke=False,
                batch_run_id=args.batch_id,
                index=idx,
                skill_source=args.skill_source,
                skill_manifest=skill_manifest,
            )
            completed += 1
            logger.info("Completed task %d: %s", idx, task_id)
        except Exception as e:
            logger.exception("Task failed: %s (index %d)", task_id, idx)
            failed.append((idx, task_id, str(e)))

    logger.info("=" * 50)
    logger.info("Batch complete: %d succeeded, %d failed", completed, len(failed))
    if failed:
        for idx, task_id, err in failed:
            logger.error("  [%d] %s: %s", idx, task_id, err[:100])
        return 1
    return 0


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    p = argparse.ArgumentParser(description="Retry specific paper arm tasks")
    p.add_argument(
        "--tasks",
        default=None,
        help="Comma-separated task indices (e.g., '9,10,11')",
    )
    p.add_argument(
        "--task-range",
        default=None,
        help="Range of task indices (e.g., '9,31' for tasks 9-31)",
    )
    p.add_argument(
        "--batch-id",
        default="sweep_v3_paper_20260416T194356Z",
        help="Batch run ID (default: sweep_v3_paper_20260416T194356Z)",
    )
    p.add_argument(
        "--registry",
        default=str(_PAPER_PB / "ldp_r_task_eval" / "r_tasks" / "registry.real.json"),
        help="Path to registry JSON",
    )
    p.add_argument(
        "--config",
        default=str(_PAPER_PB / "ldp_r_task_eval" / "config" / "pilot_openrouter.yaml"),
        help="Path to config YAML",
    )
    p.add_argument(
        "--skill-source",
        default="paper",
        choices=list(_SKILL_SOURCES),
        help="Skill source arm",
    )
    p.add_argument(
        "--skill-manifest",
        default=None,
        help="Optional skill manifest override",
    )
    p.add_argument(
        "--openrouter-key-file",
        default=str(_REPO_ROOT / "openrouterkey.txt"),
        help="Path to OpenRouter key file",
    )
    p.add_argument(
        "--key-line",
        type=int,
        default=2,
        help="Which line to read from key file (1 or 2, default: 2)",
    )
    p.add_argument(
        "--max-steps",
        type=int,
        default=15,
        help="Max steps per task (default: 15)",
    )
    p.add_argument(
        "--model",
        default="openrouter/openai/gpt-4o",
        help="Model name (default: openrouter/openai/gpt-4o)",
    )
    p.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Temperature (default: 0.1)",
    )

    ns = p.parse_args()
    raise SystemExit(asyncio.run(main_async(ns)))


if __name__ == "__main__":
    main()
