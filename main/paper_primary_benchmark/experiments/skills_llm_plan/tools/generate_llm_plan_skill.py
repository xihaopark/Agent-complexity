#!/usr/bin/env python3
"""Pre-rollout LLM-plan skill generator.

For a given R-task directory (``OBJECTIVE.md`` + ``input/`` + optional
``meta.json``), this tool makes ONE OpenRouter call and emits a SKILL.md-shaped
plan in the same 4-section layout used by paper- and pipeline-skills::

    ## Method
    ## Parameters
    ## Commands / Code Snippets
    ## Notes for R-analysis agent

Critically, the generator sees ONLY the task's own surface-level context
(objective text, input filenames + sizes + small text previews). It does NOT
read the source pipeline, method paper, or any ground-truth output — this is
the "LLM's a-priori plan forced into the skill template" arm.

CLI::

    # Single task
    python3 generate_llm_plan_skill.py \\
        --task-dir main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/<task_id> \\
        --task-id <task_id> \\
        --out-dir main/paper_primary_benchmark/experiments/skills_llm_plan/<task_id>

    # Batch over a registry
    python3 generate_llm_plan_skill.py \\
        --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json \\
        --out-root main/paper_primary_benchmark/experiments/skills_llm_plan
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path

from openai import OpenAI


SYSTEM_PROMPT = """You are preparing a SKILL.md-shaped plan for an R-centric \
analysis task. You only see the user's objective and input files (filenames, \
sizes, and short head previews for small text files). You DO NOT have the \
source pipeline, the method paper, or any ground-truth output.

Emit ONLY markdown using EXACTLY these four sections and headings, in this \
order:

## Method
1-2 short paragraphs describing the most plausible statistical / \
computational method for this task based solely on the objective text. \
If the objective explicitly names a method (e.g. DESeq2, limma, merge, \
featureCounts aggregation), center the plan on it. Do not invent methods \
that are not at least hinted at by the objective.

## Parameters
Bullet list of the tunable knobs the R script will need (e.g. thresholds \
named in the objective, column names, grouping vectors, file paths). \
Only include parameters grounded in the objective or the input preview — \
do not fabricate column names, sample labels, or thresholds.

## Commands / Code Snippets
A plausible R snippet outline if the objective implies a standard method. \
Use a fenced ```r block. Reference only column names / file paths / \
thresholds that appear in the objective or input preview. If the objective \
does not imply a standard method, write exactly: \
`(No code snippet inferred from objective.)`

## Notes for R-analysis agent
Pragmatic bullets: which R package / function is likely needed, required \
input shape, output file layout as described in the objective, and any \
pitfalls the agent should double-check. Do not reference any paper or \
external method unless it is clearly named in the objective.

Hard rules:
- Do NOT invent column names, sample identifiers, or thresholds that are \
  not present in the objective or input preview.
- Do NOT reference external papers, DOIs, authors, or pipeline source files.
- Do NOT claim knowledge of ground-truth outputs.
- Stay within the four headings above; no extra sections, no prose before \
  `## Method`.
"""


TEXT_EXTS = {".txt", ".tsv", ".csv", ".json", ".yml", ".yaml", ".md"}
BINARY_EXTS = {".bam", ".fastq.gz", ".rds", ".h5", ".png", ".pdf"}
SMALL_TEXT_BYTES = 8 * 1024
HEAD_MAX_LINES = 40
HEAD_MAX_CHARS = 2000


def _human_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n / (1024 * 1024):.2f} MB"


def _is_text_ext(name: str) -> bool:
    lname = name.lower()
    if lname.endswith(".fastq.gz"):
        return False
    for ext in TEXT_EXTS:
        if lname.endswith(ext):
            return True
    return False


def _head_preview(path: Path) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # pragma: no cover
        return f"(could not read: {exc})"
    lines = data.splitlines()
    head_lines = lines[:HEAD_MAX_LINES]
    joined = "\n".join(head_lines)
    if len(joined) > HEAD_MAX_CHARS:
        joined = joined[:HEAD_MAX_CHARS] + "\n...[truncated by char limit]"
    return joined


def _collect_input_listing(task_dir: Path) -> tuple[list[dict], list[str]]:
    """Return (listing_entries, previewed_filenames)."""
    input_dir = task_dir / "input"
    entries: list[dict] = []
    previewed: list[str] = []
    if not input_dir.is_dir():
        return entries, previewed

    for p in sorted(input_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(input_dir).as_posix()
        size = p.stat().st_size
        item: dict = {
            "path": rel,
            "size_bytes": size,
            "size_human": _human_size(size),
        }
        if _is_text_ext(p.name) and size <= SMALL_TEXT_BYTES:
            item["head"] = _head_preview(p)
            previewed.append(rel)
        entries.append(item)
    return entries, previewed


def _render_listing_block(entries: list[dict]) -> str:
    if not entries:
        return "(input/ directory is empty or missing)"
    lines = []
    for e in entries:
        lines.append(f"- `{e['path']}` — {e['size_human']} ({e['size_bytes']} bytes)")
    return "\n".join(lines)


def _render_previews_block(entries: list[dict]) -> str:
    chunks: list[str] = []
    for e in entries:
        if "head" not in e:
            continue
        chunks.append(
            f"### {e['path']}\n"
            f"(first {HEAD_MAX_LINES} lines / {HEAD_MAX_CHARS} chars max)\n\n"
            f"```\n{e['head']}\n```"
        )
    if not chunks:
        return "(no small text files to preview)"
    return "\n\n".join(chunks)


def build_user_prompt(
    task_id: str,
    objective_md: str,
    meta_obj: dict | None,
    listing: list[dict],
) -> str:
    meta_block = ""
    if meta_obj is not None:
        safe_meta = {
            k: v
            for k, v in meta_obj.items()
            if k
            in {
                "task_id",
                "kind",
                "family",
                "description",
                "success_glob",
                "reference_output_files",
            }
        }
        if safe_meta:
            meta_block = (
                "## Task metadata (safe subset)\n"
                + "```json\n"
                + json.dumps(safe_meta, indent=2)
                + "\n```\n\n"
            )

    return (
        f"Task id: `{task_id}`\n\n"
        f"{meta_block}"
        f"## OBJECTIVE.md (verbatim)\n\n"
        f"{objective_md.rstrip()}\n\n"
        f"## Input listing (under `input/`)\n\n"
        f"{_render_listing_block(listing)}\n\n"
        f"## Input schema previews (small text files only)\n\n"
        f"{_render_previews_block(listing)}\n\n"
        f"---\n"
        f"Produce the SKILL.md body now, starting with `## Method`."
    )


def call_openrouter(
    system_prompt: str,
    user_prompt: str,
    model: str,
    api_key: str,
    temperature: float,
) -> dict:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/paper2skills-ab-test",
            "X-Title": "Paper2Skills LLM-plan skill generator",
        },
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=2000,
    )
    usage = getattr(resp, "usage", None)
    return {
        "text": resp.choices[0].message.content or "",
        "usage": {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
            "completion_tokens": (
                getattr(usage, "completion_tokens", 0) if usage else 0
            ),
            "total_tokens": getattr(usage, "total_tokens", 0) if usage else 0,
        },
        "model": getattr(resp, "model", model),
    }


def load_openrouter_key(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env:
        return env
    key_file = Path(__file__).resolve().parents[4] / "openrouterkey.txt"
    if key_file.is_file():
        for line in key_file.read_text().splitlines():
            line = line.strip()
            if line:
                return line
    raise SystemExit(
        "No OpenRouter key found (env OPENROUTER_API_KEY, --api-key, or "
        f"{key_file})."
    )


def _strip_front_matter(md: str) -> str:
    if not md.startswith("---"):
        return md
    lines = md.splitlines()
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return md
    return "\n".join(lines[end_idx + 1 :]).lstrip("\n")


def generate_for_task(
    *,
    task_dir: Path,
    task_id: str,
    out_dir: Path,
    model_cli: str,
    api_key: str,
    temperature: float,
    force: bool,
) -> dict:
    """Run the generator on one task. Returns a manifest-compatible dict."""
    skill_path = out_dir / "SKILL.md"
    manifest_path = out_dir / "run_manifest.json"

    if skill_path.is_file() and not force:
        try:
            existing_manifest = json.loads(manifest_path.read_text()) if manifest_path.is_file() else {}
        except Exception:
            existing_manifest = {}
        return {
            "task_id": task_id,
            "status": "skipped_exists",
            "skill_md_path": str(skill_path),
            "run_manifest": existing_manifest,
        }

    objective_path = task_dir / "OBJECTIVE.md"
    if not objective_path.is_file():
        raise SystemExit(f"OBJECTIVE.md not found in {task_dir}")
    objective_md = objective_path.read_text(encoding="utf-8")

    meta_obj: dict | None = None
    meta_path = task_dir / "meta.json"
    if meta_path.is_file():
        try:
            meta_obj = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            meta_obj = None

    listing, previewed = _collect_input_listing(task_dir)
    inputs_listed = [e["path"] for e in listing]

    user_prompt = build_user_prompt(task_id, objective_md, meta_obj, listing)

    # OpenRouter's OpenAI-compat endpoint wants "openai/gpt-4o" style;
    # strip the optional ``openrouter/`` prefix.
    model = model_cli
    if model.startswith("openrouter/"):
        model = model.split("openrouter/", 1)[1]

    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    result = call_openrouter(
        SYSTEM_PROMPT,
        user_prompt,
        model=model,
        api_key=api_key,
        temperature=temperature,
    )
    runtime_seconds = round(time.time() - t0, 2)

    body = result["text"].strip() or "(Empty response from model.)"

    generated_at = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    skill_name = "llm-plan-" + task_id.replace("_", "-")

    previewed_yaml = "\n".join(f"  - {p}" for p in previewed) if previewed else "  []"

    frontmatter = (
        "---\n"
        f"name: {skill_name}\n"
        f"description: >-\n"
        f"  LLM-generated plan skill for task `{task_id}` (pre-rollout, "
        f"objective + inputs only; no paper or pipeline context).\n"
        f"source_type: llm_plan\n"
        f"task_id: {task_id}\n"
        f"generated_at: {generated_at}\n"
        f"model: {model_cli}\n"
        f"generator: skills_llm_plan/tools/generate_llm_plan_skill.py\n"
        f"inputs_previewed:\n{previewed_yaml}\n"
        "---\n\n"
    )
    skill_md_text = frontmatter + body + "\n"
    skill_path.write_text(skill_md_text, encoding="utf-8")

    run_manifest = {
        "task_id": task_id,
        "task_dir": str(task_dir),
        "out_dir": str(out_dir),
        "model": model_cli,
        "model_resolved": result["model"],
        "temperature": temperature,
        "prompt_tokens": result["usage"].get("prompt_tokens", 0),
        "completion_tokens": result["usage"].get("completion_tokens", 0),
        "total_tokens": result["usage"].get("total_tokens", 0),
        "runtime_seconds": runtime_seconds,
        "inputs_listed": inputs_listed,
        "inputs_previewed": previewed,
        "generated_at": generated_at,
    }
    manifest_path.write_text(
        json.dumps(run_manifest, indent=2) + "\n", encoding="utf-8"
    )

    return {
        "task_id": task_id,
        "status": "ok",
        "skill_md_path": str(skill_path),
        "skill_md_text": skill_md_text,
        "body": body,
        "run_manifest": run_manifest,
    }


def _resolve_task_dir(task: dict, repo_root: Path) -> Path:
    """Registry entries reference ``work_dir`` as a path rooted at the
    ``ldp_r_task_eval`` package. Try multiple resolutions for robustness."""
    wd = task.get("work_dir")
    if not wd:
        raise SystemExit(f"Task missing work_dir: {task}")
    candidates = [
        repo_root / "main" / "paper_primary_benchmark" / wd,
        repo_root / wd,
        Path(wd),
    ]
    for c in candidates:
        if c.is_dir():
            return c
    raise SystemExit(
        f"Could not resolve work_dir={wd} (tried: {[str(c) for c in candidates]})"
    )


def _repo_root() -> Path:
    # tools/ -> skills_llm_plan/ -> experiments/ -> paper_primary_benchmark/ ->
    # main/ -> <repo root>
    return Path(__file__).resolve().parents[5]


def _update_batch_manifest(
    manifest_path: Path,
    per_task_results: list[dict],
    model_cli: str,
    repo_root: Path,
) -> None:
    existing: dict = {"version": 1, "by_task_id": {}}
    if manifest_path.is_file():
        try:
            existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            existing = {"version": 1, "by_task_id": {}}
    existing.setdefault("version", 1)
    existing["generated_at"] = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    existing.setdefault("by_task_id", {})

    for r in per_task_results:
        if r["status"] not in {"ok", "skipped_exists"}:
            continue
        task_id = r["task_id"]
        skill_md_path = Path(r["skill_md_path"])
        try:
            rel_skill = skill_md_path.resolve().relative_to(
                (repo_root / "main" / "paper_primary_benchmark").resolve()
            ).as_posix()
        except Exception:
            rel_skill = str(skill_md_path)
        body: str = r.get("body", "")
        if not body and skill_md_path.is_file():
            body = _strip_front_matter(skill_md_path.read_text(encoding="utf-8"))
        inline = body[:4000]
        rm = r.get("run_manifest", {}) or {}
        existing["by_task_id"][task_id] = {
            "skill_md_path": rel_skill,
            "skill_md_inline": inline,
            "model": rm.get("model", model_cli),
            "prompt_tokens": rm.get("prompt_tokens", 0),
            "completion_tokens": rm.get("completion_tokens", 0),
        }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(existing, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    p = argparse.ArgumentParser(description="LLM-plan skill generator")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--task-dir",
        type=Path,
        help="Single-task mode: path to a tasks/real/<task_id> directory.",
    )
    mode.add_argument(
        "--registry",
        type=Path,
        help="Batch mode: path to registry.real.json.",
    )

    p.add_argument("--task-id", default=None, help="Required with --task-dir.")
    p.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Single-task mode: output directory. If omitted, defaults to "
        "<out-root>/<task_id>.",
    )
    p.add_argument(
        "--out-root",
        type=Path,
        default=None,
        help="Batch mode (or fallback for single): root directory under which "
        "per-task subdirs are created.",
    )
    p.add_argument("--model", default="openrouter/openai/gpt-4o")
    p.add_argument("--temperature", type=float, default=0.1)
    p.add_argument("--api-key", default=None)
    p.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing SKILL.md / run_manifest.json.",
    )
    p.add_argument(
        "--only",
        default=None,
        help="Batch: comma-separated task ids to include (default: all ready).",
    )
    args = p.parse_args()

    api_key = load_openrouter_key(args.api_key)
    repo_root = _repo_root()

    if args.task_dir is not None:
        if not args.task_id:
            raise SystemExit("--task-id is required with --task-dir")
        if args.out_dir is None:
            if args.out_root is None:
                raise SystemExit("Provide --out-dir or --out-root.")
            out_dir = args.out_root / args.task_id
        else:
            out_dir = args.out_dir

        result = generate_for_task(
            task_dir=args.task_dir,
            task_id=args.task_id,
            out_dir=out_dir,
            model_cli=args.model,
            api_key=api_key,
            temperature=args.temperature,
            force=args.force,
        )

        if args.out_root is not None:
            manifest_path = args.out_root / "manifest.json"
            _update_batch_manifest(manifest_path, [result], args.model, repo_root)

        print(
            json.dumps(
                {
                    "task_id": result["task_id"],
                    "status": result["status"],
                    "skill_md_path": result.get("skill_md_path"),
                    "run_manifest": result.get("run_manifest", {}),
                },
                indent=2,
            )
        )
        return

    if args.registry is not None:
        if args.out_root is None:
            raise SystemExit("--out-root is required with --registry.")
        reg_data = json.loads(args.registry.read_text(encoding="utf-8"))
        tasks = reg_data.get("tasks", [])
        allow = None
        if args.only:
            allow = {x.strip() for x in args.only.split(",") if x.strip()}

        results: list[dict] = []
        for t in tasks:
            if t.get("status") and t.get("status") != "ready":
                continue
            task_id = t["id"]
            if allow is not None and task_id not in allow:
                continue
            try:
                task_dir = _resolve_task_dir(t, repo_root)
            except SystemExit as e:
                print(f"[skip] {task_id}: {e}", file=sys.stderr)
                continue
            out_dir = args.out_root / task_id
            try:
                r = generate_for_task(
                    task_dir=task_dir,
                    task_id=task_id,
                    out_dir=out_dir,
                    model_cli=args.model,
                    api_key=api_key,
                    temperature=args.temperature,
                    force=args.force,
                )
            except Exception as exc:  # pragma: no cover
                print(f"[error] {task_id}: {exc}", file=sys.stderr)
                continue
            results.append(r)
            print(
                f"[{r['status']}] {task_id} -> {r.get('skill_md_path')}"
            )

        manifest_path = args.out_root / "manifest.json"
        _update_batch_manifest(manifest_path, results, args.model, repo_root)
        print(json.dumps({"batch": {"count": len(results)}}, indent=2))
        return


if __name__ == "__main__":
    main()
