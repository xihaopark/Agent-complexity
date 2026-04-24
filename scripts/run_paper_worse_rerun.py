#!/usr/bin/env python3
"""
Re-run the 4 tasks where paper performed worse than none.
Verify if fixing the skills improves performance.
"""

import sys
sys.path.insert(0, '/mnt/data1/park/Agent-complexity/scripts')

# Patch BASE_DIR for original tasks
import run_4arm_vllm_isolated
run_4arm_vllm_isolated.BASE_DIR = "/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/tasks"

from run_4arm_vllm_isolated import run_single_experiment

# Tasks where paper was worse than none
TASKS_TO_RERUN = [
    ("methylkit2tibble_split", "none", 0.692, 0.075),
    ("nearest_gene", "none", 0.889, 0.495),
    ("snakepipes_merge_ct", "none", 0.993, 0.832),
    ("snakepipes_merge_fc", "none", 0.831, 0.698),
]

print("=" * 80)
print("Re-running tasks where paper was worse than none")
print("Testing if skill fix improves performance")
print("=" * 80)

results = []
for task, baseline_arm, old_none_score, old_paper_score in TASKS_TO_RERUN:
    print(f"\n>>> {task}")
    print(f"    Previous: none={old_none_score}, paper={old_paper_score}, diff={old_paper_score-old_none_score:+.3f}")
    
    # Run paper arm with new skill
    result = run_single_experiment(task, "paper")
    results.append({
        'task': task,
        'old_none': old_none_score,
        'old_paper': old_paper_score,
        'new_paper': result['score'],
        'improvement': result['score'] - old_paper_score
    })
    
    status = "✓" if result['score'] >= old_none_score else "⚠" if result['score'] >= old_paper_score else "✗"
    print(f"    New paper score: {result['score']:.3f} {status}")
    print(f"    Improvement: {result['score'] - old_paper_score:+.3f}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\n{'Task':<25} {'Old Paper':<12} {'New Paper':<12} {'Old None':<12} {'Status':<10}")
print("-" * 80)

for r in results:
    if r['new_paper'] >= r['old_none']:
        status = "✓ FIXED"
    elif r['new_paper'] > r['old_paper']:
        status = "○ Better"
    else:
        status = "✗ Worse"
    
    print(f"{r['task']:<25} {r['old_paper']:<12.3f} {r['new_paper']:<12.3f} {r['old_none']:<12.3f} {status:<10}")

# Calculate averages
avg_old_paper = sum(r['old_paper'] for r in results) / len(results)
avg_new_paper = sum(r['new_paper'] for r in results) / len(results)
avg_old_none = sum(r['old_none'] for r in results) / len(results)

print(f"\n{'AVERAGE':<25} {avg_old_paper:<12.3f} {avg_new_paper:<12.3f} {avg_old_none:<12.3f}")

fixed_count = sum(1 for r in results if r['new_paper'] >= r['old_none'])
improved_count = sum(1 for r in results if r['new_paper'] > r['old_paper'])

print(f"\nFixed (new paper ≥ old none): {fixed_count}/4")
print(f"Improved (new > old): {improved_count}/4")

if fixed_count == 4:
    print("\n🎉 SUCCESS: All tasks fixed! Paper now performs as expected.")
elif improved_count > 0:
    print(f"\n→ PARTIAL: {improved_count} tasks improved, but need more work.")
else:
    print("\n✗ NEEDS MORE WORK: Skills still not effective.")
