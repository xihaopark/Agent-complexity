#!/usr/bin/env python3
"""
Proportional sample of 50 tasks from 145 stubs (by workflow family), prepare
self-contained micro-eval workspaces (synthetic input + OBJECTIVE + reference),
assign 5 agents × 10 tasks, and write manifests + optional registry.sample_50.json.

Does not download omics data; each task uses a deterministic mini numeric task
parallel to pilot_hello so RTaskEvalEnv experiments are runnable without Snakemake.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_LDP_EVAL = Path(__file__).resolve().parent.parent
_PAPER_PB = _LDP_EVAL.parent
_REGISTRY = _LDP_EVAL / "r_tasks" / "registry.json"
_SAMPLE_DIR = _LDP_EVAL / "experiments" / "sample_50"


def _largest_remainder_alloc(total: int, counts: dict[str, int]) -> dict[str, int]:
    """Allocate `total` seats proportionally to population counts (exact sum)."""
    pop = sum(counts.values())
    if pop == 0:
        return {}
    raw = {k: total * counts[k] / pop for k in counts}
    floors = {k: int(math.floor(raw[k])) for k in counts}
    rem = total - sum(floors.values())
    order = sorted(counts.keys(), key=lambda k: (raw[k] - floors[k]), reverse=True)
    for i in range(rem):
        floors[order[i % len(order)]] += 1
    return floors


def _values_from_task_id(task_id: str, n_lines: int = 6) -> list[int]:
    h = hashlib.sha256(task_id.encode()).digest()
    out: list[int] = []
    for i in range(n_lines):
        b = h[i % len(h)]
        out.append((b + i * 17) % 97 + 1)  # 1..97
    return out


def _write_task_files(
    stub: dict,
    *,
    agent_batch: str,
    reference_sum: int,
    values: list[int],
) -> None:
    rel = stub["work_dir"]
    root = _PAPER_PB / rel
    root.mkdir(parents=True, exist_ok=True)
    inp = root / "input"
    outd = root / "output"
    ev = root / "evaluation"
    inp.mkdir(exist_ok=True)
    outd.mkdir(exist_ok=True)
    ev.mkdir(exist_ok=True)

    (inp / "values.txt").write_text(
        "\n".join(str(x) for x in values) + "\n", encoding="utf-8"
    )
    (ev / "reference_sum.txt").write_text(str(reference_sum) + "\n", encoding="utf-8")
    (ev / "README.md").write_text(
        "Single-line `reference_sum.txt` = expected sum of integers in `input/values.txt`.\n"
        "Agent should write that decimal value as a single line in `output/result.txt`.\n",
        encoding="utf-8",
    )
    for sub in (inp, outd):
        gk = sub / ".gitkeep"
        if not gk.exists():
            gk.write_text("", encoding="utf-8")

    wf = stub.get("pipeline_workflow_id", "")
    st = stub.get("pipeline_task_id", "")
    fam = stub.get("family", "")
    objective = f"""# R-task (sample-50 micro eval)

**Pipeline provenance:** `{wf}` / `{st}` (family: `{fam}`)  
This workspace is a **self-contained numeric task** for agent/tooling experiments (not full Snakemake/omics data).

## Your goal

1. Read integers from `input/values.txt` (one per line).
2. Compute their **sum** using **R** (`run_rscript`) and/or **shell** as you prefer.
3. Write the decimal sum as **a single line** in **`output/result.txt`** (create `output/` if needed).
4. Call **`submit_done(success=true)`** only after `output/result.txt` exists and contains the correct sum.

## Acceptance

The correct answer is the sum of all integers in `input/values.txt` (deterministic for this task id). For offline scoring, see `evaluation/reference_sum.txt` (do not copy blindly; compute from data).

## Note

Large FASTQ/BAM and full pipeline assets are **not** bundled here by design; this task isolates **agent execution** in `RTaskEvalEnv`.
"""
    (root / "OBJECTIVE.md").write_text(objective.strip() + "\n", encoding="utf-8")

    meta_path = root / "meta.json"
    prev = {}
    if meta_path.is_file():
        prev = json.loads(meta_path.read_text(encoding="utf-8"))
    prev.update(
        {
            "evaluation_ready": True,
            "sample_50": True,
            "agent_batch": agent_batch,
            "prepared_at": datetime.now(timezone.utc).isoformat(),
            "micro_task": "sum_of_values_txt",
        }
    )
    meta_path.write_text(json.dumps(prev, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42, help="RNG seed for tie-break ordering")
    p.add_argument(
        "--write-registry",
        action="store_true",
        help="Also patch main registry.json: set selected tasks to ready + agent_batch",
    )
    args = p.parse_args()

    if not _REGISTRY.is_file():
        print("ERROR: missing", _REGISTRY, file=sys.stderr)
        sys.exit(1)

    reg = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    stubs = [t for t in reg["tasks"] if t.get("status") == "stub"]
    if len(stubs) != 145:
        print(f"WARN: expected 145 stubs, got {len(stubs)}", file=sys.stderr)

    by_f: dict[str, list[dict]] = defaultdict(list)
    for t in stubs:
        fam = t.get("family") or "unknown"
        by_f[fam].append(t)
    for fam in by_f:
        by_f[fam].sort(key=lambda x: x["id"])

    counts = {k: len(v) for k, v in by_f.items()}
    quota = _largest_remainder_alloc(50, counts)
    if sum(quota.values()) != 50:
        print("ERROR: quota sum != 50", quota, file=sys.stderr)
        sys.exit(1)

    selected: list[dict] = []
    rng = random.Random(args.seed)
    for fam, q in sorted(quota.items()):
        pool = by_f[fam][:]
        if len(pool) < q:
            print(f"ERROR: family {fam} only has {len(pool)} tasks, need {q}", file=sys.stderr)
            sys.exit(1)
        rng.shuffle(pool)
        selected.extend(pool[:q])

    selected.sort(key=lambda x: x["id"])
    if len(selected) != 50:
        print("ERROR: selected != 50", len(selected), file=sys.stderr)
        sys.exit(1)

    # 5 agents × 10: sequential chunks
    batches: list[tuple[str, list[dict]]] = []
    for i in range(5):
        sl = selected[i * 10 : (i + 1) * 10]
        batches.append((f"agent_{i+1:02d}", sl))

    _SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    sample_tasks_out: list[dict] = []
    for agent_id, group in batches:
        for stub in group:
            tid = stub["id"]
            vals = _values_from_task_id(tid)
            ref = sum(vals)
            _write_task_files(stub, agent_batch=agent_id, reference_sum=ref, values=vals)
            row = dict(stub)
            row["status"] = "ready"
            row["agent_batch"] = agent_id
            row["evaluation_ready"] = True
            sample_tasks_out.append(row)

    manifest = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": "50 pipeline-stage tasks with proportional family sampling; micro numeric eval",
        "seed": args.seed,
        "family_quota": quota,
        "batches": [
            {"agent_batch": aid, "task_ids": [t["id"] for t in grp]} for aid, grp in batches
        ],
    }
    (_SAMPLE_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    sample_registry = {
        "version": 1,
        "description": "Subset of 50 tasks for experiments (all ready). Paths relative to paper_primary_benchmark/.",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "tasks": sample_tasks_out,
    }
    out_reg = _LDP_EVAL / "r_tasks" / "registry.sample_50.json"
    out_reg.write_text(
        json.dumps(sample_registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if args.write_registry:
        id_to_batch = {t["id"]: t["agent_batch"] for t in sample_tasks_out}
        for t in reg["tasks"]:
            if t["id"] in id_to_batch:
                t["status"] = "ready"
                t["agent_batch"] = id_to_batch[t["id"]]
                t["evaluation_ready"] = True
        reg["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        reg["sample_50_note"] = (
            "50 tasks prepared for micro-eval; see ldp_r_task_eval/experiments/sample_50/manifest.json"
        )
        _REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Wrote:", _SAMPLE_DIR / "manifest.json")
    print("Wrote:", out_reg)
    if args.write_registry:
        print("Patched:", _REGISTRY)
    print("Agents:", [m["agent_batch"] for m in manifest["batches"]])


if __name__ == "__main__":
    main()
