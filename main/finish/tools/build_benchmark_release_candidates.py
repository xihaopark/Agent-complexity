from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_JSON = ROOT / "FINISH_EXPANSION_STATUS.json"
OUT_JSON = ROOT / "BENCHMARK_RELEASE_CANDIDATES.json"
OUT_MD = ROOT / "BENCHMARK_RELEASE_CANDIDATES.md"


def canonical_workflow_id(workflow_id: str) -> str:
    wid = str(workflow_id or "")
    if wid.endswith("-finish"):
        stem = wid[:-7]
    else:
        stem = wid
    if stem.startswith("snakemake-workflows-"):
        stem = stem[len("snakemake-workflows-"):]
    return f"{stem}-finish"


def prefer_existing(lhs: dict, rhs: dict) -> dict:
    left_id = str(lhs.get("workflow_id") or "")
    right_id = str(rhs.get("workflow_id") or "")
    left_prefixed = left_id.startswith("snakemake-workflows-")
    right_prefixed = right_id.startswith("snakemake-workflows-")
    if left_prefixed != right_prefixed:
        return rhs if left_prefixed else lhs
    return lhs if left_id <= right_id else rhs


def classify_tier(step_count: int) -> str:
    if step_count <= 4:
        return "tiny"
    if step_count <= 20:
        return "small"
    if step_count <= 40:
        return "medium"
    return "large"


def classify_family(workflow_id: str) -> str:
    wid = workflow_id.lower()
    if "scrna" in wid or "single-cell" in wid or "single_cell" in wid or "seurat" in wid or "cellranger" in wid or "cite-seq" in wid:
        return "single-cell"
    if "spatial" in wid or "slide" in wid or "astro" in wid or "sopa" in wid or "st_pipeline" in wid:
        return "spatial"
    if "atac" in wid or "chip" in wid or "methyl" in wid or "epigen" in wid:
        return "epigenomics"
    if "varseq" in wid or "dna-seq" in wid or "variant" in wid or "neoantigen" in wid or "msi" in wid:
        return "variant"
    if "rnaseq" in wid or "rna-seq" in wid or "deseq" in wid or "kallisto" in wid or "sleuth" in wid:
        return "rna"
    if "fusion" in wid or "arriba" in wid:
        return "rna"
    return "other"


def main() -> int:
    payload = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    rows = payload.get("rows") or []

    new_rows = [row for row in rows if str(row.get("workflow_id", "")).endswith("-finish")]
    passed = [row for row in new_rows if row.get("status") == "passed"]
    deduped: dict[str, dict] = {}
    for row in passed:
        canonical = canonical_workflow_id(str(row.get("workflow_id") or ""))
        if canonical in deduped:
            deduped[canonical] = prefer_existing(deduped[canonical], row)
        else:
            deduped[canonical] = row
    passed = list(deduped.values())

    release_core = []
    release_extended = []
    release_large = []

    for row in sorted(passed, key=lambda x: (int(x.get("step_count", 0)), str(x.get("workflow_id", "")))):
        workflow_id = str(row["workflow_id"])
        step_count = int(row["step_count"])
        family = classify_family(workflow_id)
        tier = classify_tier(step_count)
        record = {
            "workflow_id": workflow_id,
            "canonical_workflow_id": canonical_workflow_id(workflow_id),
            "workflow_dir": row.get("workflow_dir"),
            "status": row.get("status"),
            "step_count": step_count,
            "family": family,
            "tier": tier,
            "conversion_type": "manual-special" if workflow_id in {
                "epigen-300bcg-atacseq_pipeline-finish",
                "gammon-bio-rnaseq_pipeline-finish",
                "gersteinlab-astro-finish",
                "jfnavarro-st_pipeline-finish",
                "lwang-genomics-ngs_pipeline_sn-atac_seq-finish",
                "lwang-genomics-ngs_pipeline_sn-chip_seq-finish",
                "lwang-genomics-ngs_pipeline_sn-rna_seq-finish",
                "mohammedemamkhattabunipd-atacseq-finish",
                "saidmlonji-rnaseq_pipeline-finish",
                "tgirke-systempiperdata-chipseq-finish",
                "tgirke-systempiperdata-riboseq-finish",
                "tgirke-systempiperdata-rnaseq-finish",
                "tgirke-systempiperdata-spscrna-finish",
                "tgirke-systempiperdata-varseq-finish",
            } else "auto",
        }
        if 3 <= step_count <= 40:
            release_core.append(record)
        elif step_count > 40:
            release_large.append(record)
        else:
            release_extended.append(record)

    data = {
        "summary": {
            "total_passed": len(passed),
            "release_core_count": len(release_core),
            "release_extended_count": len(release_extended),
            "release_large_count": len(release_large),
        },
        "release_core": release_core,
        "release_extended": release_extended,
        "release_large": release_large,
    }
    OUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Benchmark Release Candidates",
        "",
        "更新日期: 2026-04-10",
        "",
        f"- 已通过 dry-run 的新增 finish workflows: {len(passed)}",
        f"- 首批核心 release 候选: {len(release_core)}",
        f"- 扩展候选: {len(release_extended)}",
        f"- 大型候选: {len(release_large)}",
        "",
        "说明:",
        "- `release_core`: 3-40 steps，优先进入首批 benchmark 对比。",
        "- `release_extended`: 2-step 或 过小 workflow，可保留作补充或 sanity check。",
        "- `release_large`: >40 steps 的大型 workflow，适合后续重负载评测。",
        "",
        "## Release Core",
        "",
        "| Workflow | Steps | Family | 类型 |",
        "|---|---:|---|---|",
    ]
    for row in release_core:
        lines.append(f"| `{row['canonical_workflow_id']}` | {row['step_count']} | {row['family']} | {row['conversion_type']} |")

    lines.extend(
        [
            "",
            "## Release Extended",
            "",
            "| Workflow | Steps | Family | 类型 |",
            "|---|---:|---|---|",
        ]
    )
    for row in release_extended:
        lines.append(f"| `{row['canonical_workflow_id']}` | {row['step_count']} | {row['family']} | {row['conversion_type']} |")

    lines.extend(
        [
            "",
            "## Release Large",
            "",
            "| Workflow | Steps | Family | 类型 |",
            "|---|---:|---|---|",
        ]
    )
    for row in release_large:
        lines.append(f"| `{row['canonical_workflow_id']}` | {row['step_count']} | {row['family']} | {row['conversion_type']} |")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_JSON)
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
