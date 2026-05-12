#!/usr/bin/env python3
"""
4-Arm Paper2Skills Experiment Runner (Direct vLLM Version)
Simplified version that directly calls vLLM API and executes R code.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Configuration
BASE_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/tasks/paper_sensitive_v1")
OUTPUT_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/runs/batch_paper2skills_v1_vllm")
SKILLS_DIR = Path("/mnt/data1/park/Agent-complexity/experiments/skills_paper2skills_v1")
VLLM_URL = "http://localhost:8000/v1/chat/completions"
VLLM_API_KEY = "local-vllm-key"
VLLM_MODEL = "qwen3-32b-local"
R_CONDA_ENV = "TS"

TASKS = [
    "deseq2_apeglm_small_n",
    "deseq2_lrt_interaction",
    "deseq2_shrinkage_comparison",
    "limma_voom_weights",
    "limma_duplicatecorrelation",
]

ARMS = ["none", "llm_plan", "pipeline", "paper"]


def load_skill(arm: str, task: str) -> Optional[str]:
    """Load skill markdown for a task-arm combination."""
    if arm == "none":
        return None
    
    skill_path = SKILLS_DIR / arm / task / "SKILL.md"
    if skill_path.exists():
        with open(skill_path) as f:
            return f.read()
    return None


def call_vllm(prompt: str, temperature: float = 0.1, max_tokens: int = 2048) -> str:
    """Call vLLM API to generate response."""
    import urllib.request
    import ssl
    
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
    
    # SSL context that accepts any cert (for local vLLM)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=300) as response:
            result = json.loads(response.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ERROR: {e}"


def generate_r_code(objective: str, skill_md: Optional[str], arm: str) -> str:
    """Generate R code using vLLM."""
    
    skill_section = ""
    if skill_md:
        skill_section = f"""

## Skill Guidance

The following guidance is provided for this task:

{skill_md}

Follow this guidance when completing the task.
"""
    
    prompt = f"""You are a bioinformatics expert. Write R code to complete the following task.

## Objective

{objective}{skill_section}

## Requirements

1. Write complete, executable R code
2. Read input data from "input/" directory (counts.tsv, coldata.tsv)
3. Write output to "output/" directory as specified in the objective
4. Include all necessary library() calls
5. Do not use Snakemake or workflow systems
6. Return ONLY the R code block, no thinking process, no explanations

IMPORTANT: Output must start immediately with ```r and end with ```. No thinking, no planning steps, no markdown headers before the code.

```r"""
    
    response = call_vllm(prompt, temperature=0.1, max_tokens=3000)
    
    # If vLLM returned an error, return it
    if response.startswith("ERROR:"):
        return response
    
    # Extract R code from response - look for the LAST code block (often after CoT)
    code = _extract_last_r_code_block(response)
    if code:
        return code
    
    # Fallback: try to find any code-like content
    # Look for lines starting with library(, counts <-, dds <-, etc.
    lines = response.split('\n')
    r_lines = []
    in_r_section = False
    for line in lines:
        # Skip thinking markers
        if any(marker in line.lower() for marker in ['okay,', 'let me', 'so ', 'therefore', 'however']):
            if not line.strip().startswith('library') and not line.strip().startswith('#'):
                continue
        # Keep R-like lines
        if any(marker in line for marker in ['library(', 'read.table', 'DESeq', 'dds <-', 'counts <-', 'write.csv', '#']):
            in_r_section = True
        if in_r_section:
            r_lines.append(line)
    
    if r_lines:
        return '\n'.join(r_lines)
    
    # Last resort: return stripped response
    return response.strip()


def _extract_last_r_code_block(text: str) -> str:
    """Extract the last R code block from text (handles CoT responses)."""
    # Find all ```r or ```R blocks and return the last one
    import re
    
    # Pattern to match ```r or ```R blocks
    pattern = r'```[rR]\n?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        # Return the last match (usually the actual code after CoT)
        code = matches[-1].strip()
        return code
    
    # Try generic code blocks
    pattern = r'```\n?(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        # Check which one looks like R code
        for match in reversed(matches):
            if any(marker in match for marker in ['library(', 'DESeq', '<-']):
                return match.strip()
    
    return None


def run_r_code(code: str, workspace: Path, timeout: int = 120) -> tuple[bool, str]:
    """Execute R code in workspace."""
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
        
        success = result.returncode == 0
        log = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nReturn code: {result.returncode}"
        return success, log
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)


def evaluate_output(task: str, workspace: Path) -> dict:
    """Evaluate agent output against reference."""
    output_dir = workspace / "output"
    ref_dir = BASE_DIR / "real_ground_truth" / task / "reference_output"
    
    if not output_dir.exists() or not ref_dir.exists():
        return {"verdict": "fail_no_output", "score": 0.0}
    
    output_files = list(output_dir.glob("*.csv"))
    ref_files = list(ref_dir.glob("*.csv"))
    
    if not output_files:
        return {"verdict": "fail_no_output", "score": 0.0}
    
    if not ref_files:
        return {"verdict": "fail_no_ref", "score": 0.0}
    
    # Check file existence and non-emptiness
    score = 0.0
    for ref_file in ref_files:
        expected_name = ref_file.name
        output_file = output_dir / expected_name
        
        # Also accept any CSV if exact name not found
        if not output_file.exists():
            for alt in output_dir.glob("*.csv"):
                if alt.stat().st_size > 50:
                    output_file = alt
                    break
        
        if output_file.exists():
            # Check file has content
            if output_file.stat().st_size > 50:  # At least some content
                score += 0.3
                # Try to validate structure
                try:
                    with open(output_file) as f:
                        lines = f.readlines()
                        if len(lines) >= 2:  # Header + at least one data row
                            score += 0.3
                            # Check header has expected DE columns
                            header = lines[0].lower()
                            if any(col in header for col in ['gene', 'base', 'log', 'pvalue', 'padj', 'fold', 'fc']):
                                score += 0.4
                except:
                    pass
    
    # Normalize score
    score = score / len(ref_files) if ref_files else 0.0
    score = min(1.0, score)
    
    if score >= 0.9:
        verdict = "pass"
    elif score >= 0.6:
        verdict = "partial"
    elif score >= 0.3:
        verdict = "attempt"
    else:
        verdict = "fail"
    
    return {"verdict": verdict, "score": score}


def run_single_experiment(task: str, arm: str) -> dict:
    """Run a single task-arm experiment."""
    print(f"\n  [{task}] [{arm}] Starting...")
    
    task_dir = BASE_DIR / "real" / task
    workspace = task_dir / "workspace"
    run_dir = OUTPUT_DIR / f"{task}_{arm}"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean workspace output
    output_dir = workspace / "output"
    if output_dir.exists():
        import shutil
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Load objective
    with open(task_dir / "OBJECTIVE.md") as f:
        objective = f.read()
    
    # Load skill
    skill_md = load_skill(arm, task)
    
    # Generate R code
    print(f"    Calling vLLM (Qwen3) for code generation...")
    start_time = time.time()
    r_code = generate_r_code(objective, skill_md, arm)
    gen_time = time.time() - start_time
    
    # Save generated code
    with open(run_dir / "generated_code.R", "w") as f:
        f.write(r_code)
    
    # Execute R code
    print(f"    Executing R code...")
    exec_start = time.time()
    success, log = run_r_code(r_code, workspace)
    exec_time = time.time() - exec_start
    
    # Save execution log
    with open(run_dir / "execution.log", "w") as f:
        f.write(log)
    
    # Evaluate
    eval_result = evaluate_output(task, workspace)
    
    # Copy outputs
    if output_dir.exists():
        import shutil
        for f in output_dir.glob("*.csv"):
            shutil.copy(f, run_dir / f.name)
    
    result = {
        "task": task,
        "arm": arm,
        "success": success,
        "gen_time": gen_time,
        "exec_time": exec_time,
        "verdict": eval_result["verdict"],
        "score": eval_result["score"],
    }
    
    status = "✓" if eval_result["verdict"] == "pass" else "○" if eval_result["verdict"] == "partial" else "✗"
    print(f"    {status} Score: {eval_result['score']:.2f}, Verdict: {eval_result['verdict']}")
    
    return result


def main():
    """Run full 4-arm experiment."""
    print("=" * 70)
    print("4-Arm Paper2Skills Experiment (Direct vLLM)")
    print(f"Model: {VLLM_MODEL}")
    print(f"Tasks: {len(TASKS)} × Arms: {len(ARMS)} = {len(TASKS) * len(ARMS)} runs")
    print("=" * 70)
    
    results = []
    
    for task in TASKS:
        print(f"\n[{task}]")
        for arm in ARMS:
            result = run_single_experiment(task, arm)
            results.append(result)
    
    # Summary
    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
    
    # Score matrix
    print("\nScore Matrix:")
    print(f"{'Task':<35} {'None':>8} {'LLMPlan':>8} {'Pipeline':>8} {'Paper':>8}")
    print("-" * 67)
    
    for task in TASKS:
        row_scores = []
        for arm in ARMS:
            score = [r["score"] for r in results if r["task"] == task and r["arm"] == arm]
            row_scores.append(score[0] if score else 0.0)
        print(f"{task:<35} {row_scores[0]:>8.2f} {row_scores[1]:>8.2f} {row_scores[2]:>8.2f} {row_scores[3]:>8.2f}")
    
    # Paper advantage analysis
    print("\nPaper Arm Advantage:")
    diffs = []
    for task in TASKS:
        task_results = [r for r in results if r["task"] == task]
        none_score = [r["score"] for r in task_results if r["arm"] == "none"][0]
        paper_score = [r["score"] for r in task_results if r["arm"] == "paper"][0]
        diff = paper_score - none_score
        diffs.append(diff)
        print(f"  {task}: {paper_score:.2f} - {none_score:.2f} = {diff:+.2f}")
    
    avg_diff = sum(diffs) / len(diffs) if diffs else 0.0
    print(f"\nAverage Paper - None difference: {avg_diff:+.2f}")
    
    if avg_diff > 0.3:
        print("🎉 SUCCESS: Paper skills show significant benefit!")
    elif avg_diff > 0.1:
        print("→ MODERATE: Paper skills show some benefit")
    else:
        print("⚠️  LOW: Paper skills benefit is limited")
    
    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results_file = OUTPUT_DIR / "experiment_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {results_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
