#!/usr/bin/env python3
"""F3 retry wrapper — re-run a subset of tasks for one arm in an existing batch.

We cannot modify ``batch_runner.py`` per F3 instructions, but the batch
runner exposes ``_one_task`` as a plain async function. This wrapper reuses
that exact function so each retried run lands under the same
``runs/batch_<batch_run_id>/<index:03d>_<task_id>/`` directory as the
original E3 sweep. Downstream tools (aggregator, V1/V2 evaluators) treat
the retried runs as native batch rows.

Usage (F3):

    python3 -m paper_primary_benchmark.experiments.llm_skill_ablation.tools.retry_paper_arm_f3 \
        --tasks snakepipes_merge_ct,riya_limma,...,clean_histoneHMM \
        --skill-source paper \
        --batch-run-id sweep_v3_paper_20260416T194356Z \
        --config experiments/llm_skill_ablation/config_e3_sweep.yaml \
        --openrouter-key-file ../openrouterkey.txt

Flags:
    --tasks            comma-separated registry task_ids to retry (required).
    --batch-run-id     batch folder suffix (must match the original sweep).
    --skill-source     one of {none,paper,pipeline,llm_plan}. Default: paper.
    --config           shared agent yaml; defaults to config_e3_sweep.yaml.
    --registry         registry JSON; defaults to registry.real.json.
    --openrouter-key-file  OpenRouter key file (first line = key).
    --skill-manifest   optional manifest override (defaults to per-arm manifest).
    --dry-run          print plan but don't run.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ABL = _HERE.parent
_PAPER_PB = _ABL.parent.parent
_MAIN = _PAPER_PB.parent
_REPO_ROOT = _MAIN.parent
if str(_MAIN) not in sys.path:
    sys.path.insert(0, str(_MAIN))

# Import batch_runner's plumbing verbatim so behaviour matches E3 exactly.
from paper_primary_benchmark.ldp_r_task_eval import batch_runner as br  # noqa: E402
from paper_primary_benchmark.ldp_r_task_eval.llm_env import (  # noqa: E402
    apply_openrouter_key_from_file,
)

logger = logging.getLogger("retry_paper_arm_f3")


def _load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


async def main_async(args: argparse.Namespace) -> int:
    cfg = br._load_yaml(Path(args.config).resolve())

    # OpenRouter key (same path as the E3 batch runner used).
    key_path = Path(args.openrouter_key_file).resolve()
    if apply_openrouter_key_from_file(key_path):
        logger.info("Set OPENROUTER_API_KEY from %s", key_path)
    elif not os.environ.get("OPENROUTER_API_KEY"):
        logger.error("OpenRouter key missing at %s", key_path)
        return 2

    reg = _load_json(Path(args.registry).resolve())
    tasks = reg.get("tasks", [])
    # Build a task_id -> (index, entry) map keyed off the canonical registry
    # order so the per-run folder stays at the same zero-padded index the E3
    # sweep used.
    by_id = {t["id"]: (i, t) for i, t in enumerate(tasks)}

    requested = [x.strip() for x in args.tasks.split(",") if x.strip()]
    missing = [t for t in requested if t not in by_id]
    if missing:
        logger.error("Unknown task_ids: %s", missing)
        return 2

    skill_source = args.skill_source
    if skill_source not in br._SKILL_SOURCES:
        logger.error("invalid --skill-source=%r", skill_source)
        return 2

    skill_manifest = None
    if skill_source != "none":
        if args.skill_manifest:
            manifest_path = Path(args.skill_manifest).resolve()
        else:
            manifest_path = br._DEFAULT_MANIFEST_BY_SOURCE[skill_source].resolve()
        if not manifest_path.is_file():
            logger.error("skill manifest missing: %s", manifest_path)
            return 2
        skill_manifest = br._load_skill_manifest(manifest_path)
        logger.info(
            "loaded skill manifest arm=%s path=%s version=%s",
            skill_source, manifest_path, skill_manifest.get("version"),
        )

    if args.dry_run:
        print("DRY-RUN plan:")
        for tid in requested:
            i, _ = by_id[tid]
            print(f"  [{i:03d}] {tid}  batch={args.batch_run_id}  arm={skill_source}")
        return 0

    ok, failed = [], []
    for tid in requested:
        idx, entry = by_id[tid]
        logger.info("retry start: arm=%s idx=%03d task=%s", skill_source, idx, tid)
        try:
            await br._one_task(
                entry,
                cfg=cfg,
                smoke=False,
                batch_run_id=args.batch_run_id,
                index=idx,
                skill_source=skill_source,
                skill_manifest=skill_manifest,
            )
            ok.append(tid)
        except Exception:
            logger.exception("retry failed: %s", tid)
            failed.append(tid)

    logger.info("retry finished: %d ok, %d durable crashes", len(ok), len(failed))
    if failed:
        logger.error("durable crashes: %s", failed)
    return 0 if not failed else 1


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="Retry subset of a sweep arm (F3)")
    p.add_argument("--tasks", required=True,
                   help="Comma-separated registry task_ids to retry")
    p.add_argument("--batch-run-id", required=True,
                   help="Batch folder suffix, e.g. sweep_v3_paper_20260416T194356Z")
    p.add_argument("--skill-source", default="paper",
                   choices=list(br._SKILL_SOURCES))
    p.add_argument("--registry",
                   default=str(_PAPER_PB / "ldp_r_task_eval" / "r_tasks" / "registry.real.json"))
    p.add_argument("--config",
                   default=str(_ABL / "config_e3_sweep.yaml"))
    p.add_argument("--openrouter-key-file",
                   default=str(_REPO_ROOT / "openrouterkey.txt"))
    p.add_argument("--skill-manifest", default=None)
    p.add_argument("--dry-run", action="store_true")
    ns = p.parse_args()
    raise SystemExit(asyncio.run(main_async(ns)))


if __name__ == "__main__":
    main()
