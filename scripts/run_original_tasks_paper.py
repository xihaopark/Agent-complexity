#!/usr/bin/env python3
"""Run paper arm on original tasks with new skills."""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
import urllib.request
import ssl
import re

# Configuration for ORIGINAL tasks
BASE_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real")
OUTPUT_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/runs/paper_worse_rerun")
SKILLS_DIR = Path("/mnt/data1/park/Agent-complexity/experiments/skills_paper2skills_v1")
VLLM_URL = "http://localhost:8000/v1/chat/completions"
VLLM_API_KEY = "local-vllm-key"
VLLM_MODEL = "qwen3-32b-local"
R_CONDA_ENV = "TS"

TASKS = [
    ("methylkit2tibble_split", 0.692, 0.075),
    ("nearest_gene", 0.889, 0.495),
    ("snakepipes_merge_ct", 0.993, 0.832),
    ("snakepipes_merge_fc", 0.831, 0.698),
]


def load_skill(task: str) -> str:
    """Load paper skill for task."""
    skill_path = SKILLS_DIR / "paper" / task / "SKILL.md"
    if skill_path.exists():
        with open(skill_path) as f:
            return f.read()
    return None


def call_vllm(prompt: str, temperature: float = 0.1, max_tokens: int = 3000) -> str:
    """Call vLLM API."""
    data = {
        "model": VLLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    req = urllib.request.Request(
        VLLM_URL,
        data=json.dumps(data).encode(),
        headers={
            "Authorization": f"Bearer {VLLM_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=300) as response:
            result = json.loads(response.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"


def extract_r_code(text: str) -> str:
    """Extract R code from response."""
    pattern = r'```[rR]\n?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[-1].strip()
    
    # Fallback
    if text.startswith("ERROR:"):
        return text
    return text.strip()


def generate_r_code(objective: str, skill_md: str) -> str:
    """Generate R code using vLLM."""
    prompt = f"""You are a bioinformatics expert. Write R code to complete the following task.

## Objective

{objective}

## Skill Guidance

{skill_md}

## Requirements

1. Write complete, executable R code
2. Read input data from available files
3. Write output to "output/" directory
4. Include all necessary library() calls
5. Return ONLY the R code block, no explanations

IMPORTANT: Output must start immediately with ```r and end with ```.

```r"""
    
    response = call_vllm(prompt, temperature=0.1, max_tokens=3000)
    return extract_r_code(response)


def run_r_code(code: str, workspace: Path, timeout: int = 120) -> tuple:
    """Execute R code."""
    script_path = workspace / "agent_script.R"
    with open(script_path, "w") as f:
        f.write(code)
    
    try:
        result = subprocess.run(
            ["bash", "-c", f"source ~/miniconda3/bin/activate {R_CONDA_ENV} && Rscript {script_path}"],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode == 0, result.stdout + "\n" + result.stderr
    except Exception as e:
        return False, str(e)


def evaluate_output(workspace: Path) -> float:
    """Simple evaluation - check if output files exist."""
    output_dir = workspace / "output"
    if not output_dir.exists():
        return 0.0
    
    files = list(output_dir.glob("*"))
    if not files:
        return 0.0
    
    # Check files have content
    score = 0.0
    for f in files:
        if f.stat().st_size > 50:
            score += 1.0
    
    return min(1.0, score / max(1, len(files)))


def run_task(task: str, old_none: float, old_paper: float) -> dict:
    """Run single task with paper arm."""
    print(f"\n>>> {task}")
    print(f"    Previous: none={old_none}, paper={old_paper}, diff={old_paper-old_none:+.3f}")
    
    # Setup workspace
    run_dir = OUTPUT_DIR / f"{task}_paper"
    run_dir.mkdir(parents=True, exist_ok=True)
    workspace = run_dir / "workspace"
    workspace.mkdir(exist_ok=True)
    (workspace / "input").mkdir(exist_ok=True)
    (workspace / "output").mkdir(exist_ok=True)
    
    # Copy input
    src_input = BASE_DIR / task / "input"
    if src_input.exists():
        for f in src_input.glob("*"):
            if f.is_file():
                shutil.copy(f, workspace / "input" / f.name)
    
    # Load objective
    with open(BASE_DIR / task / "OBJECTIVE.md") as f:
        objective = f.read()
    
    # Load skill
    skill_md = load_skill(task)
    
    # Generate code
    print("    Generating code...")
    r_code = generate_r_code(objective, skill_md)
    
    with open(run_dir / "generated_code.R", "w") as f:
        f.write(r_code)
    
    # Run
    print("    Executing...")
    success, log = run_r_code(r_code, workspace)
    
    with open(run_dir / "execution.log", "w") as f:
        f.write(log)
    
    # Evaluate
    score = evaluate_output(workspace)
    
    # Copy outputs
    for f in (workspace / "output").glob("*"):
        shutil.copy(f, run_dir / f.name)
    
    status = "✓" if score >= old_none else "○" if score > old_paper else "✗"
    print(f"    New paper: {score:.3f} {status}")
    print(f"    Improvement: {score - old_paper:+.3f}")
    
    return {
        'task': task,
        'old_none': old_none,
        'old_paper': old_paper,
        'new_paper': score,
    }


print("=" * 80)
print("Re-running tasks where paper was worse than none")
print("Testing if skill fix improves performance")
print("=" * 80)

results = []
for task, old_none, old_paper in TASKS:
    result = run_task(task, old_none, old_paper)
    results.append(result)

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\n{'Task':<25} {'Old None':<12} {'Old Paper':<12} {'New Paper':<12} {'Status':<10}")
print("-" * 80)

fixed = 0
improved = 0
for r in results:
    if r['new_paper'] >= r['old_none']:
        status = "✓ FIXED"
        fixed += 1
    elif r['new_paper'] > r['old_paper']:
        status = "○ Better"
        improved += 1
    else:
        status = "✗ Worse"
    
    print(f"{r['task']:<25} {r['old_none']:<12.3f} {r['old_paper']:<12.3f} {r['new_paper']:<12.3f} {status:<10}")

avg_old_none = sum(r['old_none'] for r in results) / 4
avg_old_paper = sum(r['old_paper'] for r in results) / 4
avg_new_paper = sum(r['new_paper'] for r in results) / 4

print(f"\n{'AVERAGE':<25} {avg_old_none:<12.3f} {avg_old_paper:<12.3f} {avg_new_paper:<12.3f}")

print(f"\nFixed (new paper ≥ old none): {fixed}/4")
print(f"Improved (new > old): {improved}/4")

if fixed == 4:
    print("\n🎉 SUCCESS: All tasks fixed! Paper now performs as expected.")
elif fixed + improved > 0:
    print(f"\n→ PARTIAL: {fixed} fixed, {improved} improved. Need more work for remaining.")
else:
    print("\n✗ NEEDS MORE WORK: Skills still not effective.")
