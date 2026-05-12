#!/usr/bin/env python3
"""Pilot driver: scripted smoke (no API) or ldp SimpleAgent + vanilla_r_task_rollout."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Allow `python .../run_pilot.py` without installing the repo as a package.
_PAPER_PB = Path(__file__).resolve().parent.parent
_MAIN = _PAPER_PB.parent
_REPO_ROOT = _MAIN.parent
if str(_MAIN) not in sys.path:
    sys.path.insert(0, str(_MAIN))

from paper_primary_benchmark.ldp_r_task_eval.llm_env import (  # noqa: E402
    apply_openrouter_key_from_file,
)

from ldp.agent.simple_agent import SimpleAgent  # noqa: E402

from paper_primary_benchmark.ldp_r_task_eval.rollout import (  # noqa: E402
    save_run_artifacts,
    scripted_success_rollout,
    vanilla_r_task_rollout,
)
from paper_primary_benchmark.ldp_r_task_eval.r_task_env import RTaskEvalEnv  # noqa: E402

logger = logging.getLogger(__name__)


def _git_sha(repo_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resolve_work_dir(cfg: dict[str, Any]) -> Path:
    rel = cfg["task"]["work_dir"]
    p = Path(rel)
    if p.is_absolute():
        return p.resolve()
    return (_PAPER_PB / p).resolve()


def _glob_from_cfg(cfg: dict[str, Any]) -> str | None:
    g = cfg.get("task", {}).get("success_artifact_glob")
    return g if g is not None else "output/result.txt"


def _base_metadata(
    task_id: str,
    work_dir: Path,
    *,
    smoke: bool,
    agent_cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = _MAIN.parent
    meta: dict[str, Any] = {
        "task_id": task_id,
        "work_dir": str(work_dir),
        "smoke": smoke,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_sha": _git_sha(repo_root),
        "python": sys.version.split()[0],
    }
    if agent_cfg is not None:
        meta["agent"] = {"llm_model": agent_cfg.get("llm_model")}
    return meta


async def _run_smoke(
    work_dir: Path,
    task_id: str,
    success_glob: str | None,
    run_dir: Path,
) -> None:
    env = RTaskEvalEnv(
        task_id=task_id,
        work_dir=work_dir,
        success_artifact_glob=success_glob,
    )
    traj = await scripted_success_rollout(env)
    meta = _base_metadata(task_id, work_dir, smoke=True)
    await save_run_artifacts(run_dir, traj, meta)
    logger.info("Wrote smoke run to %s", run_dir)


async def _run_agent(
    cfg: dict[str, Any],
    work_dir: Path,
    task_id: str,
    run_dir: Path,
) -> None:
    max_steps = int(cfg.get("max_steps", 32))
    ak = cfg.get("agent", {})
    agent = SimpleAgent(
        llm_model=ak.get("llm_model", {}),
        sys_prompt=ak.get("sys_prompt"),
    )
    env = RTaskEvalEnv(
        task_id=task_id,
        work_dir=work_dir,
        success_artifact_glob=_glob_from_cfg(cfg),
    )
    traj, _ = await vanilla_r_task_rollout(agent, env, max_steps=max_steps)
    meta = _base_metadata(task_id, work_dir, smoke=False, agent_cfg=ak)
    await save_run_artifacts(run_dir, traj, meta)
    logger.info("Wrote agent run to %s", run_dir)


async def main_async(args: argparse.Namespace) -> None:
    cfg_path = Path(args.config).resolve()
    cfg = _load_config(cfg_path)

    if not args.smoke:
        key_path = Path(args.openrouter_key_file).resolve()
        if apply_openrouter_key_from_file(key_path):
            logger.info("Set OPENROUTER_API_KEY from %s", key_path)
        elif not os.environ.get("OPENROUTER_API_KEY") and str(
            cfg.get("agent", {}).get("llm_model", {}).get("name", "")
        ).startswith("openrouter/"):
            logger.warning(
                "No OpenRouter key: file missing or empty at %s and OPENROUTER_API_KEY unset",
                key_path,
            )

    task_id = args.task_id or cfg["task"]["id"]
    work_dir = _resolve_work_dir(cfg)
    success_glob = _glob_from_cfg(cfg)

    if args.output:
        run_dir = Path(args.output).resolve()
    else:
        run_dir = (_PAPER_PB / "ldp_r_task_eval" / "runs" / args.run_id).resolve()

    if args.smoke:
        await _run_smoke(work_dir, task_id, success_glob, run_dir)
    else:
        await _run_agent(cfg, work_dir, task_id, run_dir)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    p = argparse.ArgumentParser(description="ldp R-task pilot rollout")
    p.add_argument(
        "--config",
        default=str(_PAPER_PB / "ldp_r_task_eval" / "config" / "pilot_example.yaml"),
        help="YAML config (task + agent)",
    )
    p.add_argument("--task-id", default=None, help="Override task.id from config")
    p.add_argument(
        "--smoke",
        action="store_true",
        help="No LLM: scripted write + submit_done (requires no API keys)",
    )
    p.add_argument(
        "--run-id",
        default=None,
        help="Subdirectory name under ldp_r_task_eval/runs/ (default: UTC timestamp)",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Explicit run directory (overrides --run-id)",
    )
    p.add_argument(
        "--openrouter-key-file",
        default=str(_REPO_ROOT / "openrouterkey.txt"),
        help="First line = API key; sets OPENROUTER_API_KEY for LiteLLM (ignored with --smoke)",
    )
    ns = p.parse_args()
    if ns.run_id is None:
        ns.run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    asyncio.run(main_async(ns))


if __name__ == "__main__":
    main()
