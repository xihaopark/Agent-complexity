#!/usr/bin/env python3
"""
Run only Paper arm experiments to verify skill repairs.
5 tasks × 1 arm = 5 runs
"""

import sys
sys.path.insert(0, '/mnt/data1/park/Agent-complexity/scripts')
from run_4arm_vllm_isolated import run_single_experiment

TASKS = [
    "deseq2_apeglm_small_n",
    "deseq2_lrt_interaction", 
    "deseq2_shrinkage_comparison",
    "limma_voom_weights",
    "limma_duplicatecorrelation",
]

ARM = "paper"

print("=" * 70)
print("Paper Arm Only - Skill Repair Verification")
print("=" * 70)

results = []
for task in TASKS:
    print(f"\n>>> {task} [paper]")
    result = run_single_experiment(task, ARM)
    results.append(result)
    status = "✓" if result['score'] >= 0.6 else "○" if result['score'] >= 0.3 else "✗"
    print(f"<<< {status} Score: {result['score']:.2f}, Verdict: {result['verdict']}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

avg_score = sum(r['score'] for r in results) / len(results)
success_count = sum(1 for r in results if r['score'] >= 0.6)

print(f"\nAverage Paper arm score: {avg_score:.2f}")
print(f"Successful tasks (≥0.6): {success_count}/5")

print("\nPer-task results:")
for r in results:
    status = "✓ PASS" if r['score'] >= 0.6 else "○ PARTIAL" if r['score'] >= 0.3 else "✗ FAIL"
    print(f"  {r['task']}: {r['score']:.2f} - {status}")

# Save results
import json
from pathlib import Path
OUTPUT_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/runs/batch_paper2skills_v1_vllm")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
results_file = OUTPUT_DIR / "paper_arm_results_repaired.json"
with open(results_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved: {results_file}")

if avg_score >= 0.6 and success_count >= 4:
    print("\n🎉 SUCCESS: Paper arm is working correctly!")
else:
    print("\n⚠️  NEEDS IMPROVEMENT: Some tasks still failing")
