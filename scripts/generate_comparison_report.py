#!/usr/bin/env python3
"""Generate 4-arm comparison report from evaluation results."""

import json
import pandas as pd
from pathlib import Path
import argparse

def load_evaluation(eval_dir: Path, task: str, arm: str) -> dict:
    """Load evaluation result for a task-arm combination."""
    # Try multiple naming patterns
    patterns = [
        eval_dir / f"{task}_{arm}.json",
        eval_dir / f"{task}/{arm}/evaluation.json",
        eval_dir / f"batch_{task}_{arm}.json",
    ]
    
    for pattern in patterns:
        if pattern.exists():
            with open(pattern) as f:
                return json.load(f)
    
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, help="Batch run ID")
    parser.add_argument("--output", required=True, help="Output report markdown file")
    args = parser.parse_args()
    
    # Configuration
    tasks = [
        "deseq2_apeglm_small_n",
        "deseq2_lrt_interaction", 
        "deseq2_shrinkage_comparison",
        "limma_voom_weights",
        "limma_duplicatecorrelation",
    ]
    arms = ["none", "llm_plan", "pipeline", "paper"]
    
    eval_dir = Path(f"main/paper_primary_benchmark/ldp_r_task_eval/runs/_evaluations/{args.batch}")
    
    # Collect results
    results = []
    for task in tasks:
        for arm in arms:
            data = load_evaluation(eval_dir, task, arm)
            if data:
                results.append({
                    "task": task,
                    "arm": arm,
                    "score": data.get("overall_score", 0),
                    "verdict": data.get("verdict", "unknown"),
                })
            else:
                results.append({
                    "task": task,
                    "arm": arm,
                    "score": 0,
                    "verdict": "missing",
                })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    pivot = df.pivot(index="task", columns="arm", values="score")
    
    # Calculate differences
    diff_pp = pivot["paper"] - pivot["none"]
    diff_pl = pivot["paper"] - pivot["llm_plan"]
    diff_pi = pivot["paper"] - pivot["pipeline"]
    
    # Generate report
    report = f"""# 4-Arm Experiment Report: {args.batch}

## Score Matrix

| Task | None | LLM_Plan | Pipeline | Paper | Paper-None | Paper-Pipeline |
|------|------|----------|----------|-------|-----------|---------------|
"""
    
    for task in tasks:
        if task in pivot.index:
            row = pivot.loc[task]
            report += f"| {task} | {row['none']:.3f} | {row['llm_plan']:.3f} | {row['pipeline']:.3f} | **{row['paper']:.3f}** | {diff_pp[task]:+.3f} | {diff_pi[task]:+.3f} |\n"
    
    # Summary statistics
    report += f"""
## Summary Statistics

| Metric | Value |
|--------|-------|
| Mean Paper score | {pivot['paper'].mean():.3f} |
| Mean None score | {pivot['none'].mean():.3f} |
| **Mean Paper-None diff** | **{diff_pp.mean():.3f}** |
| Mean Paper-Pipeline diff | {diff_pi.mean():.3f} |
| Tasks with diff > 0.5 | {(diff_pp > 0.5).sum()}/{len(tasks)} |

## Interpretation

- **Paper-None diff > 0.5**: Indicates paper skill provides significant benefit
- **Paper-Pipeline diff > 0.3**: Indicates paper skill is better than generic code templates
- **Target**: All 5 tasks should have Paper-None diff >= 0.5

## Detailed Results

"""
    
    for task in tasks:
        report += f"\n### {task}\n\n"
        task_df = df[df["task"] == task]
        for _, row in task_df.iterrows():
            report += f"- **{row['arm']}**: {row['score']:.3f} ({row['verdict']})\n"
    
    # Write report
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    
    print(f"✓ Report written to: {output_path}")
    print(f"\nKey finding: Mean Paper-None difference = {diff_pp.mean():.3f}")
    
    if diff_pp.mean() > 0.5:
        print("🎉 SUCCESS: Paper skills show significant benefit!")
    else:
        print("⚠️  Paper skills benefit is smaller than expected. Review tasks/skill extraction.")

if __name__ == "__main__":
    main()
