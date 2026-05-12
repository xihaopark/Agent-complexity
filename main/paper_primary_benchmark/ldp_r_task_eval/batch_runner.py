#!/usr/bin/env python3
"""Batch rollout over `r_tasks/registry.json` (optional; same CLI patterns as run_pilot)."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

_PAPER_PB = Path(__file__).resolve().parent.parent
_MAIN = _PAPER_PB.parent
_REPO_ROOT = _MAIN.parent
if str(_MAIN) not in sys.path:
    sys.path.insert(0, str(_MAIN))

from ldp.agent.simple_agent import SimpleAgent  # noqa: E402

from paper_primary_benchmark.ldp_r_task_eval.llm_env import (  # noqa: E402
    apply_openrouter_key_from_file,
)
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


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_registry(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _resolve_work_dir(entry: dict[str, Any]) -> Path:
    rel = entry["work_dir"]
    p = Path(rel)
    if p.is_absolute():
        return p.resolve()
    return (_PAPER_PB / p).resolve()


_SKILL_PLACEHOLDER = "{{SKILL_MD}}"
_NO_SKILL_MARKER = "(No paper-derived skill is available for this task.)"

_SKILL_SOURCES = ("none", "paper", "pipeline", "llm_plan")

_PAPER_SKILLS_ROOT = _PAPER_PB / "experiments" / "skills"
_PIPELINE_SKILLS_ROOT = _PAPER_PB / "experiments" / "skills_pipeline"
_LLM_PLAN_SKILLS_ROOT = _PAPER_PB / "experiments" / "skills_llm_plan"

_DEFAULT_MANIFEST_BY_SOURCE: dict[str, Path] = {
    "paper": _PAPER_SKILLS_ROOT / "manifest.json",
    "pipeline": _PIPELINE_SKILLS_ROOT / "manifest.json",
    "llm_plan": _LLM_PLAN_SKILLS_ROOT / "manifest.json",
}


def _load_skill_manifest(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _strip_skill_md_front_matter(text: str) -> str:
    """Strip YAML front matter + optional ``` ```markdown ``` fence from
    SKILL.md so the body matches what ``skill_md_inline`` contains in the
    per-task manifests."""
    t = text.lstrip()
    if t.startswith("---"):
        closing = t.find("\n---", 3)
        if closing != -1:
            nl = t.find("\n", closing + 4)
            t = t[nl + 1:] if nl != -1 else t[closing + 4:]
    t = t.lstrip()
    if t.startswith("```markdown"):
        t = t[len("```markdown"):].lstrip("\n")
        tail = t.rfind("```")
        if tail != -1:
            t = t[:tail]
    return t.strip()


def _registry_workflow_id(entry: dict[str, Any]) -> str | None:
    """Detect whichever field the registry uses to name the source workflow.

    The V2 registry (`registry.real.json`) uses ``pipeline_workflow_id``;
    older / alternative schemas may use ``workflow_id`` or ``pipeline``.
    """
    for k in ("workflow_id", "pipeline_workflow_id"):
        v = entry.get(k)
        if isinstance(v, str) and v:
            return v
    p = entry.get("pipeline")
    if isinstance(p, dict) and isinstance(p.get("workflow_id"), str):
        return p["workflow_id"]
    return None


def _resolve_task_skill(
    *,
    skill_source: str,
    manifest: dict[str, Any] | None,
    registry_entry: dict[str, Any],
    task_id: str,
) -> tuple[str, dict[str, Any]]:
    """Return ``(skill_text, skill_meta)`` for a given arm / task.

    ``skill_text`` is always safe to splice into a sys_prompt template —
    it falls back to ``_NO_SKILL_MARKER`` when no skill is found. ``skill_meta``
    always carries at least ``{"arm": <skill_source>, "injected": bool}``.
    """
    base_meta: dict[str, Any] = {"arm": skill_source}
    if skill_source == "none":
        return _NO_SKILL_MARKER, {**base_meta, "injected": False}

    manifest = manifest or {}
    manifest_version = manifest.get("version")
    inline: str | None = None
    entry: dict[str, Any] | None = None
    lookup_field: str | None = None
    lookup_key: str | None = None

    if skill_source in ("paper", "llm_plan"):
        per_task = manifest.get("by_task_id") or {}
        entry = per_task.get(task_id)
        lookup_field = "by_task_id"
        lookup_key = task_id
        if entry and entry.get("skill_md_inline"):
            inline = entry["skill_md_inline"]

    # Paper fallback: manifest-level by_task_id is only populated for a few
    # curated tasks, but `by_workflow_id` covers every paper-covered workflow
    # with a DOI slug → disk-resident SKILL.md. Synthesize the inline text on
    # the fly so all 6 curated tasks resolve.
    if skill_source == "paper" and inline is None:
        wf = _registry_workflow_id(registry_entry)
        by_wf = manifest.get("by_workflow_id") or {}
        raw = by_wf.get(wf) if wf else None
        doi: str | None = None
        if isinstance(raw, list) and raw:
            doi = raw[0]
        elif isinstance(raw, dict):
            doi = raw.get("source_doi") or raw.get("doi")
        elif isinstance(raw, str):
            doi = raw
        if doi:
            skill_file = _PAPER_SKILLS_ROOT / doi / "SKILL.md"
            if skill_file.is_file():
                inline = _strip_skill_md_front_matter(
                    skill_file.read_text(encoding="utf-8")
                )
                rel_path = skill_file.relative_to(_REPO_ROOT).as_posix()
                entry = {
                    "source_doi": doi.replace("_", "/", 1),
                    "skill_md_path": rel_path,
                    "pipeline_workflow_id": wf,
                }
                lookup_field = "by_workflow_id"
                lookup_key = wf

    if skill_source == "pipeline":
        wf = _registry_workflow_id(registry_entry)
        by_wf = manifest.get("by_workflow_id") or {}
        entry = by_wf.get(wf) if wf else None
        lookup_field = "by_workflow_id"
        lookup_key = wf
        if isinstance(entry, dict) and entry.get("skill_md_inline"):
            inline = entry["skill_md_inline"]

    if inline is None:
        meta: dict[str, Any] = {
            **base_meta,
            "injected": False,
            "reason": "no_skill_for_task",
            "manifest_version": manifest_version,
            "lookup_field": lookup_field,
            "lookup_key": lookup_key,
        }
        return _NO_SKILL_MARKER, meta

    sha = hashlib.sha256(inline.encode("utf-8")).hexdigest()
    meta = {
        **base_meta,
        "injected": True,
        "manifest_version": manifest_version,
        "skill_sha256": sha,
        "skill_char_len": len(inline),
        "skill_md_path": (entry or {}).get("skill_md_path"),
        "lookup_field": lookup_field,
        "lookup_key": lookup_key,
    }
    if skill_source == "paper":
        meta["source_doi"] = (entry or {}).get("source_doi")
        if (entry or {}).get("source_tool"):
            meta["source_tool"] = entry["source_tool"]
        if (entry or {}).get("pipeline_workflow_id"):
            meta["source_workflow_id"] = entry["pipeline_workflow_id"]
    elif skill_source == "pipeline":
        meta["source_workflow_id"] = lookup_key
    elif skill_source == "llm_plan":
        meta["source_task_id"] = task_id
        if (entry or {}).get("model"):
            meta["source_model"] = entry["model"]
    return inline, meta


def _render_sys_prompt(
    template: str | None,
    skill_text: str,
    skill_source: str,
) -> str | None:
    """Substitute ``{{SKILL_MD}}`` in the configured sys_prompt template.

    - On ``skill_source='none'`` we still substitute with ``_NO_SKILL_MARKER``
      to keep prompt shape stable across arms (same rule used in Phase 1).
    - If the template has no placeholder we leave it alone — the user opted
      into a skill source but the config is static; failing loudly later is
      preferable to silent no-op rendering.
    """
    if template is None:
        return None
    if _SKILL_PLACEHOLDER not in template:
        return template
    return template.replace(
        _SKILL_PLACEHOLDER, skill_text or _NO_SKILL_MARKER
    )


async def _one_task(
    entry: dict[str, Any],
    *,
    cfg: dict[str, Any],
    smoke: bool,
    batch_run_id: str,
    index: int,
    skill_source: str = "none",
    skill_manifest: dict[str, Any] | None = None,
) -> None:
    task_id = entry["id"]
    canonical_work_dir = _resolve_work_dir(entry)
    glob = entry.get("success_artifact_glob", "output/result.txt")
    run_dir = (
        _PAPER_PB
        / "ldp_r_task_eval"
        / "runs"
        / f"batch_{batch_run_id}"
        / f"{index:03d}_{task_id}"
    )
    run_dir = run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    # Per-run isolated workspace copy. We copy only agent-visible files so that
    # two arms (e.g., no-skill vs with-skill) cannot overwrite each other.
    work_dir = run_dir / "workspace"
    if work_dir.exists():
        shutil.rmtree(work_dir)
    shutil.copytree(canonical_work_dir, work_dir, symlinks=False)

    if smoke:
        env = RTaskEvalEnv(
            task_id=task_id,
            work_dir=work_dir,
            success_artifact_glob=glob,
        )
        traj = await scripted_success_rollout(env)
        meta = {
            "task_id": task_id,
            "canonical_work_dir": str(canonical_work_dir),
            "work_dir": str(work_dir),
            "smoke": True,
            "batch_run_id": batch_run_id,
            "registry_index": index,
            "git_sha": _git_sha(_MAIN.parent),
        }
        await save_run_artifacts(run_dir, traj, meta)
        logger.info("smoke ok: %s -> %s", task_id, run_dir)
        return

    max_steps = int(cfg.get("max_steps", 32))
    ak = cfg.get("agent", {})
    sys_prompt_template = ak.get("sys_prompt")
    skill_text, skill_meta = _resolve_task_skill(
        skill_source=skill_source,
        manifest=skill_manifest,
        registry_entry=entry,
        task_id=task_id,
    )
    sys_prompt = _render_sys_prompt(
        sys_prompt_template, skill_text, skill_source
    )
    if skill_meta.get("injected"):
        logger.info(
            "skill injected: arm=%s task=%s key=%s/%s sha256=%s",
            skill_meta.get("arm"),
            task_id,
            skill_meta.get("lookup_field"),
            skill_meta.get("lookup_key"),
            (skill_meta.get("skill_sha256") or "")[:12],
        )
    else:
        logger.info(
            "skill NOT injected: arm=%s task=%s reason=%s",
            skill_meta.get("arm"),
            task_id,
            skill_meta.get("reason", "arm_none"),
        )
    agent = SimpleAgent(
        llm_model=ak.get("llm_model", {}),
        sys_prompt=sys_prompt,
    )
    env = RTaskEvalEnv(
        task_id=task_id,
        work_dir=work_dir,
        success_artifact_glob=glob,
    )
    traj, _ = await vanilla_r_task_rollout(agent, env, max_steps=max_steps)
    meta = {
        "task_id": task_id,
        "canonical_work_dir": str(canonical_work_dir),
        "work_dir": str(work_dir),
        "smoke": False,
        "batch_run_id": batch_run_id,
        "registry_index": index,
        "git_sha": _git_sha(_MAIN.parent),
        "agent": {"llm_model": ak.get("llm_model")},
    }
    meta["skill"] = skill_meta
    await save_run_artifacts(run_dir, traj, meta)
    logger.info("agent ok: %s -> %s", task_id, run_dir)


async def main_async(args: argparse.Namespace) -> int:
    cfg = _load_yaml(Path(args.config).resolve())
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

    reg = _load_registry(Path(args.registry).resolve())
    tasks = reg.get("tasks", [])
    batch_run_id = args.batch_run_id or datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    # Back-compat: legacy callers that only pass `--skill-manifest <path>`
    # (no explicit `--skill-source`) are treated as the paper arm.
    skill_source = args.skill_source
    if skill_source is None:
        skill_source = "paper" if args.skill_manifest else "none"
    if skill_source not in _SKILL_SOURCES:
        logger.error(
            "invalid --skill-source=%r (expected one of %s)",
            skill_source,
            ",".join(_SKILL_SOURCES),
        )
        return 2

    skill_manifest: dict[str, Any] | None = None
    if skill_source != "none":
        if args.skill_manifest:
            manifest_path = Path(args.skill_manifest).resolve()
        else:
            default = _DEFAULT_MANIFEST_BY_SOURCE[skill_source]
            manifest_path = default.resolve()
        if not manifest_path.is_file():
            logger.error(
                "skill manifest not found for arm=%s: %s",
                skill_source,
                manifest_path,
            )
            return 2
        skill_manifest = _load_skill_manifest(manifest_path)
        n_task = len(skill_manifest.get("by_task_id", {}) or {})
        n_wf = len(skill_manifest.get("by_workflow_id", {}) or {})
        logger.info(
            "loaded skill manifest: arm=%s path=%s version=%s (by_task_id=%d, by_workflow_id=%d)",
            skill_source,
            manifest_path,
            skill_manifest.get("version"),
            n_task,
            n_wf,
        )
    else:
        logger.info("skill arm=none (no manifest loaded)")

    failed: list[str] = []
    for i, entry in enumerate(tasks):
        tid = entry.get("id", str(i))
        try:
            await _one_task(
                entry,
                cfg=cfg,
                smoke=args.smoke,
                batch_run_id=batch_run_id,
                index=i,
                skill_source=skill_source,
                skill_manifest=skill_manifest,
            )
        except Exception:
            logger.exception("task failed: %s", tid)
            failed.append(tid)

    n_ok = len(tasks) - len(failed)
    if failed:
        logger.error(
            "batch finished: %d ok, %d failed; failed ids: %s",
            n_ok,
            len(failed),
            failed[:50],
        )
        if len(failed) > 50:
            logger.error("... and %d more", len(failed) - 50)
        return 1
    logger.info("batch finished: %d tasks ok", n_ok)
    return 0


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    p = argparse.ArgumentParser(description="Batch ldp R-task rollouts from r_tasks/registry.json")
    p.add_argument(
        "--registry",
        default=str(_PAPER_PB / "ldp_r_task_eval" / "r_tasks" / "registry.json"),
        help="JSON registry (tasks[].id, work_dir, success_artifact_glob)",
    )
    p.add_argument(
        "--config",
        default=str(_PAPER_PB / "ldp_r_task_eval" / "config" / "pilot_example.yaml"),
        help="YAML shared agent + max_steps",
    )
    p.add_argument(
        "--smoke",
        action="store_true",
        help="Scripted success path per task (no LLM)",
    )
    p.add_argument(
        "--batch-run-id",
        default=None,
        help="Folder name under runs/batch_<id>/ (default: UTC timestamp)",
    )
    p.add_argument(
        "--openrouter-key-file",
        default=str(_REPO_ROOT / "openrouterkey.txt"),
        help="First line = key; sets OPENROUTER_API_KEY (ignored with --smoke)",
    )
    p.add_argument(
        "--skill-source",
        default=None,
        choices=list(_SKILL_SOURCES),
        help=(
            "Which skill source to inject into the {{SKILL_MD}} placeholder. "
            "Defaults to 'none' (no injection). If omitted while "
            "--skill-manifest is set, behaves as 'paper' for back-compat."
        ),
    )
    p.add_argument(
        "--skill-manifest",
        default=None,
        help=(
            "Optional override for the manifest path. When omitted and "
            "--skill-source != none, the default manifest for the chosen "
            "arm is loaded: "
            "paper=experiments/skills/manifest.json, "
            "pipeline=experiments/skills_pipeline/manifest.json, "
            "llm_plan=experiments/skills_llm_plan/manifest.json. "
            "Ignored with --smoke."
        ),
    )
    ns = p.parse_args()
    raise SystemExit(asyncio.run(main_async(ns)))


if __name__ == "__main__":
    main()
