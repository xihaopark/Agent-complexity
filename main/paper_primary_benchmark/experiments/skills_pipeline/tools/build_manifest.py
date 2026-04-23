#!/usr/bin/env python3
"""Assemble ``experiments/skills_pipeline/manifest.json`` from per-workflow outputs."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


WORKFLOW_IDS = [
    "akinyi-onyango-rna_seq_pipeline-finish",
    "rna-seq-star-deseq2-finish",
    "fritjoflammers-snakemake-methylanalysis-finish",
    "lwang-genomics-ngs_pipeline_sn-rna_seq-finish",
    "cellranger-multi-finish",
    "epigen-rnaseq_pipeline-finish",
    "cite-seq-alevin-fry-seurat-finish",
    "read-alignment-pangenome-finish",
]


FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n+", re.DOTALL)


def strip_front_matter(md: str) -> str:
    body = FRONT_MATTER_RE.sub("", md, count=1)
    body = body.lstrip()
    if body.startswith("```markdown"):
        first_nl = body.find("\n")
        if first_nl != -1:
            body = body[first_nl + 1 :]
        if body.rstrip().endswith("```"):
            body = body.rstrip()[:-3].rstrip() + "\n"
    return body


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    # root = experiments/skills_pipeline
    by_workflow: dict[str, dict] = {}
    skipped: list[dict] = []

    for wid in WORKFLOW_IDS:
        wf_dir = root / wid
        skill_path = wf_dir / "SKILL.md"
        run_path = wf_dir / "run_manifest.json"
        if not run_path.is_file():
            skipped.append({"workflow_id": wid, "reason": "run_manifest.json missing"})
            continue
        run_manifest = json.loads(run_path.read_text(encoding="utf-8"))
        status = run_manifest.get("status")
        if status != "ok" or not skill_path.is_file():
            skipped.append(
                {
                    "workflow_id": wid,
                    "reason": run_manifest.get("reason")
                    or f"status={status}, SKILL.md missing={not skill_path.is_file()}",
                }
            )
            continue

        skill_md = skill_path.read_text(encoding="utf-8")
        body = strip_front_matter(skill_md)
        inline = body[:4000]

        files_considered = run_manifest.get("files_considered", [])
        files_included = run_manifest.get("files_included", [])

        by_workflow[wid] = {
            "skill_md_path": f"experiments/skills_pipeline/{wid}/SKILL.md",
            "skill_md_inline": inline,
            "source_files_considered": len(files_considered),
            "source_files_count": len(files_included),
            "source_chars_used": run_manifest.get("chars_used", 0),
            "truncated": run_manifest.get("truncated", False),
            "model": run_manifest.get("model", "openrouter/openai/gpt-4o"),
            "prompt_tokens": run_manifest.get("prompt_tokens", 0),
            "completion_tokens": run_manifest.get("completion_tokens", 0),
            "runtime_seconds": run_manifest.get("runtime_seconds", 0.0),
            "workflow_dir": run_manifest.get("workflow_dir", ""),
        }

    manifest = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "experiments/skills_pipeline/tools/build_manifest.py",
        "by_workflow_id": by_workflow,
        "workflows_skipped": skipped,
        "notes": (
            "Built by Subagent B2 from per-workflow run_manifest.json outputs. "
            "skill_md_inline is SKILL.md with YAML front matter (and any leading "
            "```markdown fence) stripped, truncated to 4000 chars. "
            "source_files_count is the number of files actually sent to the LLM "
            "(<= files_considered)."
        ),
    }

    out_path = root / "manifest.json"
    out_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"wrote {out_path} ({len(by_workflow)} workflows, {len(skipped)} skipped)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
