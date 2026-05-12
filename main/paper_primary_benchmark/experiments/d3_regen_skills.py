#!/usr/bin/env python3
"""D3 driver: regenerate paper, pipeline, llm_plan skills + manifests for V3."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # paper_primary_benchmark/
REPO = ROOT.parents[1]
LIT_MAP = ROOT / "literature" / "workflow_literature_map.json"
LIT_PDFS = ROOT / "literature" / "pdfs"
SKILLS_DIR = ROOT / "experiments" / "skills"
SKILLS_PIPELINE_DIR = ROOT / "experiments" / "skills_pipeline"
SKILLS_LLM_DIR = ROOT / "experiments" / "skills_llm_plan"
REGISTRY = ROOT / "ldp_r_task_eval" / "r_tasks" / "registry.real.json"

VISION_ADAPTER = ROOT / "experiments" / "paper2skills_ab_test" / "vision_adapter.py"
PIPELINE_TOOL = SKILLS_PIPELINE_DIR / "tools" / "generate_pipeline_skill.py"
LLM_TOOL = SKILLS_LLM_DIR / "tools" / "generate_llm_plan_skill.py"

WORKFLOW_DIRS = {
    "akinyi-onyango-rna_seq_pipeline-finish": "Akinyi-Onyango__rna_seq_pipeline",
    "rna-seq-star-deseq2-finish": "snakemake-workflows__rna-seq-star-deseq2",
    "fritjoflammers-snakemake-methylanalysis-finish": "fritjoflammers__snakemake-methylanalysis",
    "snakemake-workflows-rna-longseq-de-isoform": "snakemake-workflows__rna-longseq-de-isoform",
    "maxplanck-ie-snakepipes-finish": "maxplanck-ie__snakePipes",
    "RiyaDua-cervical-cancer-snakemake-workflow": "RiyaDua__cervical-cancer-snakemake-workflow",
    "snakemake-workflows-chipseq-finish": "snakemake-workflows__chipseq",
    "epigen-spilterlize_integrate-finish": "epigen__spilterlize_integrate",
    "epigen-dea_limma-finish": "epigen__dea_limma",
    "snakemake-workflows-msisensor-pro-finish": "snakemake-workflows__microsatellite-instability-detection-with-msisensor-pro",
    "joncahn-epigeneticbutton-finish": "joncahn__epigeneticbutton",
}


def doi_safe(doi: str) -> str:
    return doi.replace("/", "_")


def load_map() -> dict:
    return json.loads(LIT_MAP.read_text())


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text())


def strip_front_matter(md: str) -> str:
    t = md.lstrip()
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


def generate_paper_skills() -> dict:
    """Generate paper SKILL.md for each unique DOI in literature map v3 with a
    local PDF. Returns summary dict."""
    lit = load_map()
    summary = {"generated": [], "skipped_existing": [], "skipped_no_pdf": [], "by_workflow_id": {}, "by_doi": {}}

    unique_dois: dict[str, dict] = {}
    for wf in lit["workflows"]:
        doi = wf.get("primary_doi")
        wid = wf["workflow_id"]
        if not doi:
            summary["skipped_no_pdf"].append(wid + " (no primary_doi)")
            continue
        ds = doi_safe(doi)
        pdf = LIT_PDFS / f"{ds}.pdf"
        if not pdf.is_file() or pdf.stat().st_size == 0:
            summary["skipped_no_pdf"].append(f"{wid} (missing PDF {pdf.name})")
            continue
        unique_dois.setdefault(ds, {"doi": doi, "pdf": pdf, "primary_tool": wf.get("primary_tool"), "workflow_ids": []})
        unique_dois[ds]["workflow_ids"].append(wid)

    for ds, info in unique_dois.items():
        out_dir = SKILLS_DIR / ds
        skill_md = out_dir / "SKILL.md"
        if skill_md.is_file():
            summary["skipped_existing"].append(ds)
        else:
            print(f"[paper] generating {ds} (pdf={info['pdf'].name}) for workflows: {info['workflow_ids']}")
            out_dir.mkdir(parents=True, exist_ok=True)
            cmd = [
                sys.executable, str(VISION_ADAPTER),
                "--pdf", str(info["pdf"]),
                "--out-dir", str(out_dir),
            ]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"[paper] ERROR generating {ds}: {r.stderr[:500]}")
                continue
            summary["generated"].append(ds)
        try:
            body = strip_front_matter(skill_md.read_text())
            rm = {}
            rmp = out_dir / "run_manifest.json"
            if rmp.is_file():
                rm = json.loads(rmp.read_text())
        except Exception:
            body = ""
            rm = {}
        summary["by_doi"][ds] = {
            "skill_md_path": f"experiments/skills/{ds}/SKILL.md",
            "skill_md_inline": body[:4000],
            "source_doi": info["doi"],
            "source_tool": info.get("primary_tool"),
            "workflow_ids": info["workflow_ids"],
            "pages_processed": rm.get("pages_processed"),
            "model": rm.get("model"),
            "prompt_tokens": rm.get("usage", {}).get("prompt_tokens"),
            "completion_tokens": rm.get("usage", {}).get("completion_tokens"),
        }
        for wid in info["workflow_ids"]:
            summary["by_workflow_id"].setdefault(wid, []).append(ds)

    return summary


def build_paper_manifest(paper_summary: dict) -> None:
    """Rewrite experiments/skills/manifest.json v3. Preserve any v2 entries we
    have SKILL.md on disk for."""
    reg = load_registry()
    by_workflow_id: dict[str, list[str]] = dict(paper_summary["by_workflow_id"])

    # Preserve pre-existing skills whose DOIs aren't yet covered (e.g. v2 entries
    # for workflows not in the literature map's primary_doi list). We only keep
    # ones that have a SKILL.md on disk.
    if (SKILLS_DIR / "manifest.json").is_file():
        try:
            old = json.loads((SKILLS_DIR / "manifest.json").read_text())
            for wid, dois in (old.get("by_workflow_id") or {}).items():
                if wid in by_workflow_id:
                    continue
                dlist = dois if isinstance(dois, list) else [dois]
                kept = [d for d in dlist if (SKILLS_DIR / d / "SKILL.md").is_file()]
                if kept:
                    by_workflow_id[wid] = kept
        except Exception:
            pass

    # Build by_task_id (registry tasks whose workflow_id has paper coverage)
    by_task_id: dict[str, dict] = {}
    for t in reg["tasks"]:
        wid = t.get("pipeline_workflow_id")
        dois = by_workflow_id.get(wid)
        if not dois:
            continue
        ds = dois[0]
        sdata = paper_summary["by_doi"].get(ds)
        if not sdata:
            # Use filesystem SKILL.md
            skp = SKILLS_DIR / ds / "SKILL.md"
            if skp.is_file():
                body = strip_front_matter(skp.read_text())
                sdata = {
                    "skill_md_path": f"experiments/skills/{ds}/SKILL.md",
                    "skill_md_inline": body[:4000],
                    "source_doi": ds.replace("_", "/", 1),
                    "source_tool": None,
                }
            else:
                continue
        by_task_id[t["id"]] = {
            "skill_md_path": sdata["skill_md_path"],
            "skill_md_inline": sdata["skill_md_inline"],
            "source_doi": sdata.get("source_doi"),
            "source_tool": sdata.get("source_tool"),
            "pipeline_workflow_id": wid,
        }

    tasks_without_skill = [
        t["id"] for t in reg["tasks"] if t.get("pipeline_workflow_id") not in by_workflow_id
    ]

    manifest = {
        "version": 3,
        "generated_at": "2026-04-17",
        "by_workflow_id": by_workflow_id,
        "by_task_id": by_task_id,
        "by_doi": paper_summary["by_doi"],
        "tasks_without_skill": tasks_without_skill,
        "notes": (
            "V3 paper-skills manifest generated by D3. skill_md_inline is "
            "SKILL.md with YAML front matter (and any leading ```markdown "
            "fence) stripped, truncated to 4000 chars. by_workflow_id keys "
            "use literature_map workflow_ids; note that registry "
            "'pipeline_workflow_id' may differ for some entries (e.g. "
            "'snakemake-workflows-msisensor-pro-finish' vs "
            "'microsatellite-instability-detection-with-msisensor-pro-finish')."
        ),
    }

    # Emit aliases so the batch_runner's pipeline_workflow_id lookup resolves.
    # The literature map uses slightly different ids in a couple of cases.
    aliases = {
        "snakemake-workflows-msisensor-pro-finish":
            "microsatellite-instability-detection-with-msisensor-pro-finish",
    }
    for reg_wid, lit_wid in aliases.items():
        if reg_wid in by_workflow_id:
            continue
        if lit_wid in by_workflow_id:
            manifest["by_workflow_id"][reg_wid] = list(by_workflow_id[lit_wid])

    # Re-derive tasks_without_skill after aliases
    manifest["tasks_without_skill"] = [
        t["id"] for t in reg["tasks"]
        if t.get("pipeline_workflow_id") not in manifest["by_workflow_id"]
    ]
    # Re-derive by_task_id for aliased tasks too
    for t in reg["tasks"]:
        if t["id"] in manifest["by_task_id"]:
            continue
        wid = t.get("pipeline_workflow_id")
        dois = manifest["by_workflow_id"].get(wid)
        if not dois:
            continue
        ds = dois[0]
        skp = SKILLS_DIR / ds / "SKILL.md"
        if not skp.is_file():
            continue
        body = strip_front_matter(skp.read_text())
        manifest["by_task_id"][t["id"]] = {
            "skill_md_path": f"experiments/skills/{ds}/SKILL.md",
            "skill_md_inline": body[:4000],
            "source_doi": ds.replace("_", "/", 1),
            "source_tool": manifest["by_doi"].get(ds, {}).get("source_tool"),
            "pipeline_workflow_id": wid,
        }

    (SKILLS_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    print(f"[paper] wrote manifest with {len(manifest['by_workflow_id'])} workflow ids, "
          f"{len(manifest['by_task_id'])} tasks covered, "
          f"{len(manifest['tasks_without_skill'])} tasks without paper")


def generate_pipeline_skills() -> dict:
    reg = load_registry()
    workflow_ids = sorted({t["pipeline_workflow_id"] for t in reg["tasks"]})
    summary = {"generated": [], "skipped_existing": [], "missing_source": []}
    for wid in workflow_ids:
        out_dir = SKILLS_PIPELINE_DIR / wid
        skill = out_dir / "SKILL.md"
        if skill.is_file():
            summary["skipped_existing"].append(wid)
            continue
        subdir = WORKFLOW_DIRS.get(wid)
        if not subdir:
            summary["missing_source"].append(wid + " (no mapping)")
            continue
        wf_dir = REPO / "main" / "finish" / "workflow_candidates" / subdir
        if not wf_dir.is_dir():
            summary["missing_source"].append(f"{wid} ({wf_dir} not found)")
            continue
        print(f"[pipeline] generating {wid} from {subdir}")
        cmd = [
            sys.executable, str(PIPELINE_TOOL),
            "--workflow-dir", str(wf_dir),
            "--workflow-id", wid,
            "--out-dir", str(out_dir),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[pipeline] ERROR {wid}: {r.stderr[:500]}")
            continue
        summary["generated"].append(wid)
    return summary


def build_pipeline_manifest() -> None:
    reg = load_registry()
    workflow_ids = sorted({t["pipeline_workflow_id"] for t in reg["tasks"]})
    by_workflow_id: dict = {}

    # Preserve v2 entries (keep non-registry workflow keys too)
    existing_path = SKILLS_PIPELINE_DIR / "manifest.json"
    existing = {}
    if existing_path.is_file():
        try:
            existing = json.loads(existing_path.read_text())
        except Exception:
            existing = {}
    for wid, entry in (existing.get("by_workflow_id") or {}).items():
        skp = ROOT.parent.parent / entry["skill_md_path"] if isinstance(entry, dict) and "skill_md_path" in entry else None
        if isinstance(entry, dict) and entry.get("skill_md_path"):
            by_workflow_id[wid] = entry

    for wid in workflow_ids:
        out_dir = SKILLS_PIPELINE_DIR / wid
        skill_md = out_dir / "SKILL.md"
        run_manifest = out_dir / "run_manifest.json"
        if not skill_md.is_file():
            continue
        body = strip_front_matter(skill_md.read_text())
        rm = {}
        if run_manifest.is_file():
            try:
                rm = json.loads(run_manifest.read_text())
            except Exception:
                rm = {}
        by_workflow_id[wid] = {
            "skill_md_path": f"experiments/skills_pipeline/{wid}/SKILL.md",
            "skill_md_inline": body[:4000],
            "source_files_considered": len(rm.get("files_considered", [])) if isinstance(rm.get("files_considered"), list) else rm.get("source_files_considered"),
            "source_files_count": len(rm.get("files_included", [])) if isinstance(rm.get("files_included"), list) else rm.get("source_files_count"),
            "source_chars_used": rm.get("chars_used") or rm.get("source_chars_used"),
            "truncated": rm.get("truncated"),
            "model": rm.get("model"),
            "prompt_tokens": rm.get("prompt_tokens"),
            "completion_tokens": rm.get("completion_tokens"),
            "runtime_seconds": rm.get("runtime_seconds") or rm.get("llm_seconds"),
            "workflow_dir": rm.get("workflow_dir"),
        }

    manifest = {
        "version": 3,
        "generated_at": "2026-04-17",
        "generator": "experiments/skills_pipeline/tools/generate_pipeline_skill.py (D3 wrapper)",
        "by_workflow_id": by_workflow_id,
        "workflows_skipped": [],
        "notes": (
            "V3 pipeline-skills manifest: covers every workflow_id referenced "
            "in registry.real.json (32 tasks across 11 workflows), plus v2 "
            "legacy entries. skill_md_inline is SKILL.md with front matter "
            "stripped, truncated to 4000 chars."
        ),
    }
    existing_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"[pipeline] wrote manifest with {len(by_workflow_id)} workflow ids")


def generate_llm_plan_skills() -> dict:
    cmd = [
        sys.executable, str(LLM_TOOL),
        "--registry", str(REGISTRY),
        "--out-root", str(SKILLS_LLM_DIR),
    ]
    print("[llm_plan] running batch generator")
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout[-4000:])
    if r.returncode != 0:
        print(f"[llm_plan] ERROR: {r.stderr[-2000:]}")
    # Post-process: manifest is updated in-place by the tool; just annotate version
    mp = SKILLS_LLM_DIR / "manifest.json"
    if mp.is_file():
        m = json.loads(mp.read_text())
        m["version"] = 3
        m["generated_at_v3"] = "2026-04-17"
        m["notes"] = (
            "V3 llm-plan-skills manifest: covers every task in registry.real.json. "
            "Regenerated from 2026-04-17 batch via generate_llm_plan_skill.py."
        )
        mp.write_text(json.dumps(m, indent=2) + "\n")
    return {"ok": r.returncode == 0, "stdout": r.stdout[-2000:]}


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--step", choices=["paper", "pipeline", "llm", "all"], default="all")
    args = p.parse_args()

    if args.step in ("paper", "all"):
        s = generate_paper_skills()
        build_paper_manifest(s)
        print(f"[paper] generated={len(s['generated'])} skipped_existing={len(s['skipped_existing'])} skipped_no_pdf={len(s['skipped_no_pdf'])}")
    if args.step in ("pipeline", "all"):
        s = generate_pipeline_skills()
        build_pipeline_manifest()
        print(f"[pipeline] generated={len(s['generated'])} skipped_existing={len(s['skipped_existing'])} missing={len(s['missing_source'])}")
        for m in s["missing_source"]:
            print(f"  missing_source: {m}")
    if args.step in ("llm", "all"):
        generate_llm_plan_skills()


if __name__ == "__main__":
    main()
