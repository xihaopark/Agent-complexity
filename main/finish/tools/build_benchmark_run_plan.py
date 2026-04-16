from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_JSON = ROOT / "BENCHMARK_RELEASE_CANDIDATES.json"
OUT_JSON = ROOT / "BENCHMARK_RUN_PLAN.json"
OUT_MD = ROOT / "BENCHMARK_RUN_PLAN.md"


def canonical_workflow_id(workflow_id: str) -> str:
    wid = str(workflow_id or "")
    if wid.endswith("-finish"):
        stem = wid[:-7]
    else:
        stem = wid
    if stem.startswith("snakemake-workflows-"):
        stem = stem[len("snakemake-workflows-"):]
    return f"{stem}-finish"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total", type=int, default=12)
    parser.add_argument("--max-per-family", type=int, default=3)
    parser.add_argument("--include-large", action="store_true")
    return parser.parse_args()


def score(row: dict) -> tuple:
    step_count = int(row["step_count"])
    conversion_rank = 0 if row.get("conversion_type") == "auto" else 1
    family = row.get("family", "other")
    family_rank = {
        "rna": 0,
        "single-cell": 1,
        "epigenomics": 2,
        "variant": 3,
        "spatial": 4,
        "other": 5,
    }.get(family, 9)
    # Prefer moderate-size workflows for the first formal run
    distance_from_mid = abs(step_count - 18)
    return (family_rank, distance_from_mid, conversion_rank, step_count, row["workflow_id"])


def main() -> int:
    args = parse_args()
    payload = json.loads(RELEASE_JSON.read_text(encoding="utf-8"))
    core = list(payload.get("release_core") or [])
    large = list(payload.get("release_large") or [])

    candidates = sorted(core, key=score)
    if args.include_large:
        candidates.extend(sorted(large, key=lambda x: (x.get("family", "other"), int(x["step_count"]))))

    selected: list[dict] = []
    family_counts: dict[str, int] = defaultdict(int)
    for row in candidates:
        family = row.get("family", "other")
        if family_counts[family] >= args.max_per_family:
            continue
        selected.append(row)
        family_counts[family] += 1
        if len(selected) >= args.max_total:
            break
    for row in selected:
        row["canonical_workflow_id"] = canonical_workflow_id(str(row.get("workflow_id") or ""))

    plan = {
        "summary": {
            "max_total": args.max_total,
            "max_per_family": args.max_per_family,
            "include_large": args.include_large,
            "selected_count": len(selected),
            "family_counts": dict(family_counts),
        },
        "selected_workflows": selected,
    }
    OUT_JSON.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Benchmark Run Plan",
        "",
        "更新日期: 2026-04-10",
        "",
        f"- 计划工作流数量: {len(selected)}",
        f"- 每个家族上限: {args.max_per_family}",
        f"- 是否包含 large 集合: {args.include_large}",
        "",
        "选择原则:",
        "- 优先选择 `release_core` 中 steps 适中的 workflow。",
        "- 尽量覆盖 `rna` / `single-cell` / `epigenomics` / `variant` / `spatial` / `other` 各家族。",
        "- 每个家族默认不超过 3 个，避免首轮实验过于偏向单一领域。",
        "",
        "## 选中 workflow",
        "",
        "| Workflow | Steps | Family | 类型 |",
        "|---|---:|---|---|",
    ]
    for row in selected:
        lines.append(
            f"| `{row['canonical_workflow_id']}` | {row['step_count']} | {row['family']} | {row['conversion_type']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT_JSON)
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
