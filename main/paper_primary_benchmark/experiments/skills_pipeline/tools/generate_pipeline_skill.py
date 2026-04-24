#!/usr/bin/env python3
"""Pipeline-source skill generator for Paper2Skills.

Companion to ``experiments/paper2skills_ab_test/vision_adapter.py``. Instead of
rendering a paper's PDF pages to a vision model, this reads the *source code* of
a workflow (Snakefiles, R scripts, Python scripts, config/env YAMLs, READMEs)
and asks an OpenRouter text model (default ``openai/gpt-4o``) to distil a
SKILL.md with the same four sections the vision adapter produces
(Method / Parameters / Commands / Notes).

CLI::

    python generate_pipeline_skill.py \\
        --workflow-dir main/finish/workflow_candidates/<repo> \\
        --workflow-id <workflow_id> \\
        --out-dir main/paper_primary_benchmark/experiments/skills_pipeline/<workflow_id> \\
        [--model openrouter/openai/gpt-4o] [--max-per-file 8000] [--max-total 80000]

Outputs under ``--out-dir``:
- ``SKILL.md`` with YAML front matter and the 4-section body.
- ``run_manifest.json`` with token usage, runtime, files considered/included.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI


SYSTEM_PROMPT = """You are Paper2Skill (pipeline-source mode). You will read \
the concatenated source files of a bioinformatics analysis pipeline (Snakemake \
rules, R / Rmd scripts, Python scripts, configuration YAMLs, and READMEs) and \
distil them into a SKILL.md that another LLM agent will consume when asked to \
re-run the pipeline's analysis in R. Base every claim on what the source \
actually shows; if a detail is not in the provided files, say so instead of \
inventing it.

Respond with ONLY markdown using EXACTLY these four sections and headings, in \
this order:

## Method
1-3 paragraphs describing what the pipeline does end-to-end: the biological \
question, the statistical or computational method(s) it implements (e.g. \
STAR + DESeq2, alevin-fry + Seurat, MethylKit, etc.), and any key assumptions \
or choices the source makes.

## Parameters
Bulleted list of the tunable parameters / config keys the pipeline exposes \
(name, default if present in the source, meaning). Prefer values that appear \
in ``config*.yaml`` or a Snakefile ``params:`` block. Only state defaults that \
are actually written in the files.

## Commands / Code Snippets
Copy the most useful R / shell / Python snippets verbatim inside fenced code \
blocks with the correct language tag. Favour the R / Rmd analysis steps (the \
downstream agent runs R tasks). If no R code is evident anywhere in the \
provided source, write exactly:

    (No R code snippets visible in the pipeline source.)

Do NOT invent R code that is not present.

## Notes for R-analysis agent
Pragmatic bullets: which R package / function implements each analysis step, \
expected input shapes, pitfalls from the pipeline's config, and anything the \
agent should double-check (e.g. required metadata columns, reference genome, \
normalization choice) before reporting results.
"""


INCLUDE_EXT_PRIORITY: list[tuple[int, list[str]]] = [
    (0, ["snakefile", ".smk", ".snakefile"]),
    (1, [".r", ".rmd"]),
    (2, [".py"]),
    (3, [".yaml", ".yml"]),
    (4, ["readme"]),
]

MAX_RAW_BYTES = 100 * 1024  # skip files larger than 100 KB raw


def classify(path: Path) -> tuple[int, str] | None:
    """Return (priority, kind) if ``path`` should be considered, else None."""
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name == "snakefile" or suffix in {".smk", ".snakefile"}:
        return (0, "snakefile")
    if suffix in {".r", ".rmd"}:
        return (1, "r")
    if suffix == ".py":
        return (2, "python")
    if suffix in {".yaml", ".yml"}:
        if (
            name.startswith("config")
            or name.startswith("environment")
            or name.startswith("env")
        ):
            return (3, "yaml")
        return None
    if name.startswith("readme"):
        return (4, "readme")
    return None


def collect_files(root: Path) -> list[tuple[int, str, Path, int]]:
    """Return sorted ``(priority, kind, path, raw_bytes)`` entries under ``root``."""
    entries: list[tuple[int, str, Path, int]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        # Skip hidden dirs like .git, .snakemake, .github noise except README.
        parts = path.relative_to(root).parts
        if any(
            part in {".git", ".snakemake", ".venv", "__pycache__", "node_modules"}
            for part in parts
        ):
            continue
        info = classify(path)
        if info is None:
            continue
        priority, kind = info
        try:
            size = path.stat().st_size
        except OSError:
            continue
        entries.append((priority, kind, path, size))
    # Stable sort: priority, then relative path for deterministic order.
    entries.sort(key=lambda e: (e[0], str(e[2])))
    return entries


def build_blob(
    entries: list[tuple[int, str, Path, int]],
    root: Path,
    max_per_file: int,
    max_total: int,
) -> tuple[str, list[dict], list[dict], bool]:
    """Concatenate files into a single blob with separators.

    Returns ``(blob, files_considered, files_included, truncated)``.
    """
    files_considered: list[dict] = []
    files_included: list[dict] = []
    pieces: list[str] = []
    total = 0
    truncated = False
    for priority, kind, path, size in entries:
        rel = str(path.relative_to(root))
        considered = {
            "path": rel,
            "kind": kind,
            "bytes": size,
            "priority": priority,
        }
        files_considered.append(considered)
        if size > MAX_RAW_BYTES:
            considered["skipped"] = "too_large"
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            considered["skipped"] = f"read_error: {exc}"
            continue
        used = text[:max_per_file]
        if len(text) > max_per_file:
            used += f"\n... (truncated, showed {max_per_file}/{len(text)} chars)\n"
        header = f"\n=== FILE: {rel} ===\n"
        chunk = header + used
        if total + len(chunk) > max_total:
            remaining = max_total - total
            if remaining > len(header) + 200:
                pieces.append(chunk[:remaining])
                files_included.append(
                    {
                        "path": rel,
                        "kind": kind,
                        "chars_used": remaining - len(header),
                        "partial": True,
                    }
                )
                total = max_total
            truncated = True
            break
        pieces.append(chunk)
        total += len(chunk)
        files_included.append(
            {
                "path": rel,
                "kind": kind,
                "chars_used": len(used),
                "partial": len(text) > max_per_file,
            }
        )
    return "".join(pieces), files_considered, files_included, truncated


def load_openrouter_key(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env:
        return env
    # Repo layout: .../Paper2Skills-main/main/paper_primary_benchmark/experiments/skills_pipeline/tools/<this file>
    key_file = Path(__file__).resolve().parents[5] / "openrouterkey.txt"
    if key_file.is_file():
        for line in key_file.read_text().splitlines():
            line = line.strip()
            if line:
                return line
    raise SystemExit(
        "No OpenRouter key found (env OPENROUTER_API_KEY, --api-key, or "
        f"{key_file})."
    )


def call_openrouter(
    blob: str, workflow_id: str, model: str, api_key: str
) -> dict:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/paper2skills-ab-test",
            "X-Title": "Paper2Skills pipeline-source adapter",
        },
    )
    user_msg = (
        f"Workflow id: {workflow_id}\n"
        f"The following is the concatenated source of the pipeline, with "
        f"`=== FILE: <relpath> ===` separators. Extract the 4 sections as "
        f"specified.\n\n"
        f"{blob}"
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.2,
        max_tokens=2500,
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


def main() -> int:
    p = argparse.ArgumentParser(description="Pipeline-source SKILL.md generator")
    p.add_argument("--workflow-dir", type=Path, required=True)
    p.add_argument("--workflow-id", required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--model", default="openrouter/openai/gpt-4o")
    p.add_argument("--max-per-file", type=int, default=8000)
    p.add_argument("--max-total", type=int, default=80000)
    p.add_argument("--api-key", default=None)
    p.add_argument(
        "--min-blob-chars",
        type=int,
        default=1024,
        help="If the collected blob is smaller than this, skip and write a "
        "stub manifest with status='skipped_empty'.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Collect files and print stats, do not call the LLM.",
    )
    args = p.parse_args()

    if not args.workflow_dir.is_dir():
        print(f"ERROR: workflow dir not found: {args.workflow_dir}", file=sys.stderr)
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    entries = collect_files(args.workflow_dir)
    blob, considered, included, truncated = build_blob(
        entries, args.workflow_dir, args.max_per_file, args.max_total
    )
    blob_len = len(blob)

    dropped_chars = sum(
        e[3] for e in entries if e[3] <= MAX_RAW_BYTES
    ) - sum(f.get("chars_used", 0) for f in included)
    # Note: entry sizes are raw bytes, included chars are post-decode; the diff
    # is only a rough indicator of what we left on the floor.
    print(
        f"[collect] workflow={args.workflow_id} considered={len(considered)} "
        f"included={len(included)} blob_chars={blob_len} truncated={truncated} "
        f"approx_dropped={max(dropped_chars, 0)}"
    )

    if blob_len < args.min_blob_chars:
        run_manifest = {
            "workflow_id": args.workflow_id,
            "workflow_dir": str(args.workflow_dir),
            "out_dir": str(args.out_dir),
            "status": "skipped_empty",
            "reason": f"blob {blob_len} chars < min_blob_chars {args.min_blob_chars}",
            "files_considered": considered,
            "files_included": included,
            "truncated": truncated,
            "model": args.model,
            "runtime_seconds": round(time.time() - t0, 2),
        }
        (args.out_dir / "run_manifest.json").write_text(
            json.dumps(run_manifest, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(run_manifest, indent=2))
        return 0

    if args.dry_run:
        print("[dry-run] skipping LLM call")
        (args.out_dir / "run_manifest.json").write_text(
            json.dumps(
                {
                    "workflow_id": args.workflow_id,
                    "status": "dry_run",
                    "files_considered": considered,
                    "files_included": included,
                    "chars_used": blob_len,
                    "truncated": truncated,
                    "model": args.model,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        return 0

    api_key = load_openrouter_key(args.api_key)
    model = args.model
    if model.startswith("openrouter/"):
        model = model.split("openrouter/", 1)[1]

    t1 = time.time()
    result = call_openrouter(blob, args.workflow_id, model=model, api_key=api_key)
    t_llm = time.time() - t1

    body = result["text"].strip() or "(Empty response from model.)"
    # Strip any leading ```markdown fence the model sometimes wraps around
    # its answer; keep internal fenced code blocks intact.
    stripped = body
    if stripped.startswith("```"):
        first_nl = stripped.find("\n")
        if first_nl != -1:
            stripped = stripped[first_nl + 1 :]
        if stripped.rstrip().endswith("```"):
            stripped = stripped.rstrip()[:-3].rstrip() + "\n"
    body = stripped

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    skill_name = "pipeline-" + args.workflow_id
    frontmatter = (
        "---\n"
        f"name: {skill_name}\n"
        "source_type: pipeline\n"
        f"workflow_id: {args.workflow_id}\n"
        f"workflow_dir: {args.workflow_dir}\n"
        f"generated_at: {generated_at}\n"
        f"model: {args.model}\n"
        f"files_used: {len(included)}\n"
        f"chars_used: {blob_len}\n"
        "generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py\n"
        "---\n\n"
    )
    skill_md = frontmatter + body.rstrip() + "\n"
    (args.out_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    manifest = {
        "workflow_id": args.workflow_id,
        "workflow_dir": str(args.workflow_dir),
        "out_dir": str(args.out_dir),
        "status": "ok",
        "generated_at": generated_at,
        "model": args.model,
        "resolved_model": result["model"],
        "max_per_file": args.max_per_file,
        "max_total": args.max_total,
        "prompt_tokens": result["usage"]["prompt_tokens"],
        "completion_tokens": result["usage"]["completion_tokens"],
        "total_tokens": result["usage"]["total_tokens"],
        "runtime_seconds": round(time.time() - t0, 2),
        "llm_seconds": round(t_llm, 2),
        "chars_used": blob_len,
        "truncated": truncated,
        "files_considered": considered,
        "files_included": included,
    }
    (args.out_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in manifest.items() if k not in {"files_considered", "files_included"}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
