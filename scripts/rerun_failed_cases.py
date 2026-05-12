#!/usr/bin/env python3
"""Rerun failed cases to get better results."""

import sys
import shutil
from pathlib import Path

sys.path.insert(0, '/mnt/data1/park/Agent-complexity/scripts')
from run_4arm_vllm_isolated import run_single_experiment

# Cases to rerun (those with issues)
CASES_TO_RERUN = [
    # deseq2_apeglm_small_n - paper and pipeline failed
    ("deseq2_apeglm_small_n", "paper"),
    ("deseq2_apeglm_small_n", "pipeline"),
    
    # limma_voom_weights - all failed
    ("limma_voom_weights", "none"),
    ("limma_voom_weights", "llm_plan"),
    ("limma_voom_weights", "pipeline"),
    ("limma_voom_weights", "paper"),
    
    # deseq2_shrinkage_comparison - all failed
    ("deseq2_shrinkage_comparison", "none"),
    ("deseq2_shrinkage_comparison", "llm_plan"),
    ("deseq2_shrinkage_comparison", "pipeline"),
    ("deseq2_shrinkage_comparison", "paper"),
]

OUTPUT_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/runs/batch_paper2skills_v1_vllm")

print("=" * 70)
print("RE-RUNNING FAILED CASES")
print("=" * 70)

results = []
for task, arm in CASES_TO_RERUN:
    run_dir = OUTPUT_DIR / f"{task}_{arm}"
    
    # Backup old run
    if run_dir.exists():
        backup_dir = OUTPUT_DIR / f"{task}_{arm}_backup"
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.move(run_dir, backup_dir)
        print(f"\nBacked up {task}_{arm}")
    
    # Rerun
    print(f"\n>>> Re-running: {task} [{arm}]")
    result = run_single_experiment(task, arm)
    results.append(result)
    print(f"<<< Result: score={result['score']}, verdict={result['verdict']}")

print("\n" + "=" * 70)
print("RE-RUN COMPLETE")
print("=" * 70)

# Show comparison
print("\nBefore vs After:")
for task, arm in CASES_TO_RERUN:
    backup_file = OUTPUT_DIR / f"{task}_{arm}_backup" / "experiment_result.json"
    # Read old result from main results file
    import json
    with open(OUTPUT_DIR / "experiment_results.json") as f:
        all_results = json.load(f)
    
    old = [r for r in all_results if r['task'] == task and r['arm'] == arm]
    new = [r for r in results if r['task'] == task and r['arm'] == arm]
    
    old_score = old[0]['score'] if old else 0
    new_score = new[0]['score'] if new else 0
    
    change = "↑" if new_score > old_score else "↓" if new_score < old_score else "="
    print(f"  {task}[{arm}]: {old_score:.2f} → {new_score:.2f} {change}")

# Update main results file
with open(OUTPUT_DIR / "experiment_results.json") as f:
    all_results = json.load(f)

# Replace with new results
for new_r in results:
    for i, old_r in enumerate(all_results):
        if old_r['task'] == new_r['task'] and old_r['arm'] == new_r['arm']:
            all_results[i] = new_r
            break

with open(OUTPUT_DIR / "experiment_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print(f"\nUpdated results saved to: {OUTPUT_DIR / 'experiment_results.json'}")
