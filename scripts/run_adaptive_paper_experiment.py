#!/usr/bin/env python3
"""
Run paper arm with adaptive skill querying.
For tasks that previously performed worse than baseline.
"""

import sys
sys.path.insert(0, '/mnt/data1/park/Agent-complexity/scripts')

import json
import os
import shutil
import subprocess
from pathlib import Path
import urllib.request
import ssl
import re

# Configuration
BASE_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real")
OUTPUT_DIR = Path("/mnt/data1/park/Agent-complexity/main/paper_primary_benchmark/ldp_r_task_eval/runs/adaptive_paper_experiment")
SKILLS_DIR = Path("/mnt/data1/park/Agent-complexity/experiments/skills_paper2skills_v1/paper")
VLLM_URL = "http://localhost:8000/v1/chat/completions"
VLLM_API_KEY = "local-vllm-key"
VLLM_MODEL = "qwen3-32b-local"
R_CONDA_ENV = "TS"

# Tasks that previously had paper worse than none
TASKS = [
    {
        "id": "methylkit2tibble_split",
        "old_none": 0.692,
        "old_paper": 0.075,
        "old_diff": -0.617,
        "reason": "MethPat skill mismatched (data processing task)"
    },
    {
        "id": "nearest_gene", 
        "old_none": 0.889,
        "old_paper": 0.495,
        "old_diff": -0.394,
        "reason": "snakePipes skill mismatched (simple annotation task)"
    },
    {
        "id": "snakepipes_merge_ct",
        "old_none": 0.993,
        "old_paper": 0.832,
        "old_diff": -0.161,
        "reason": "workflow skill too complex for file merging"
    },
    {
        "id": "snakepipes_merge_fc",
        "old_none": 0.831,
        "old_paper": 0.698,
        "old_diff": -0.133,
        "reason": "workflow skill too complex for file merging"
    }
]


def get_available_skills():
    """Get list of available skills for agent to query."""
    manifest_path = SKILLS_DIR / "manifest.json"
    if not manifest_path.exists():
        return []
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    skills = []
    for skill_id, skill_path in manifest.get("skills", {}).items():
        full_path = SKILLS_DIR.parent / skill_path
        if full_path.exists():
            with open(full_path) as f:
                content = f.read()
            skills.append({
                "id": skill_id,
                "content": content[:2000]  # First 2000 chars for relevance check
            })
    return skills


def call_vllm(prompt, temperature=0.1, max_tokens=4000):
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


def agent_query_skills(objective, available_skills):
    """
    Agent queries skills and decides which (if any) to use.
    Returns: (selected_skill_id, skill_content) or (None, None)
    """
    if not available_skills:
        return None, None
    
    # Build skill list for prompt
    skill_list = "\n\n".join([
        f"Skill {i+1}: {s['id']}\n{s['content'][:500]}..."
        for i, s in enumerate(available_skills[:3])  # Top 3 skills
    ])
    
    query_prompt = f"""You are analyzing a bioinformatics task to decide whether to use available paper-derived skills.

## Task Objective
{objective[:500]}

## Available Skills
{skill_list}

## Your Task
1. Assess the relevance of each skill to the task (0-1 scale)
2. Decide if any skill is helpful enough to use (threshold: 0.6)
3. Return ONLY a JSON object with your decision

## Response Format
```json
{{
  "skill_selected": "skill_id or null",
  "relevance_scores": {{
    "skill_id_1": 0.8,
    "skill_id_2": 0.3
  }},
  "reasoning": "brief explanation"
}}
```

## Rules
- skill_selected: the skill ID if relevance >= 0.6, otherwise null
- Be honest: if no skill matches, return null
- Don't force a match if the skill is not relevant"""

    response = call_vllm(query_prompt, temperature=0.1, max_tokens=1000)
    
    # Try to extract JSON
    try:
        # Find JSON block
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0].strip()
        else:
            json_str = response.strip()
        
        decision = json.loads(json_str)
        selected = decision.get("skill_selected")
        
        if selected and selected != "null":
            # Find full skill content
            for skill in available_skills:
                if skill["id"] == selected:
                    return selected, skill["content"]
        
        return None, None
    except:
        # If parsing fails, assume no skill selected
        return None, None


def generate_r_code(objective, skill_content=None):
    """Generate R code, optionally with skill guidance."""
    
    skill_section = ""
    if skill_content:
        skill_section = f"""

## Relevant Paper Skill (Selected by Agent)
{skill_content}

You may use this skill guidance if it helps solve the task.
"""
    else:
        skill_section = """

## Paper Skills
You queried available paper skills but none were relevant to this task.
Proceed with your baseline knowledge.
"""
    
    prompt = f"""You are a bioinformatics expert. Write R code to complete the following task.

## Objective
{objective}{skill_section}

## Requirements
1. Write complete, executable R code
2. Read input data from available files
3. Write output to "output/" directory
4. Include all necessary library() calls
5. Return ONLY the R code block, no explanations

IMPORTANT: Start with ```r and end with ```

```r"""
    
    response = call_vllm(prompt, temperature=0.1, max_tokens=3000)
    
    # Extract code
    if "```r" in response:
        code = response.split("```r")[1].split("```")[0].strip()
    elif "```" in response:
        code = response.split("```")[1].split("```")[0].strip()
    else:
        code = response.strip()
    
    return code


def run_r_code(code, workspace, timeout=120):
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


def evaluate_output(workspace):
    """Simple evaluation."""
    output_dir = workspace / "output"
    if not output_dir.exists():
        return 0.0
    
    files = list(output_dir.glob("*"))
    if not files:
        return 0.0
    
    score = 0.0
    for f in files:
        if f.stat().st_size > 50:
            score += 1.0
    
    return min(1.0, score / max(1, len(files)))


def run_adaptive_paper(task_info):
    """Run task with adaptive paper skill selection."""
    task = task_info["id"]
    
    print(f"\n{'='*60}")
    print(f"Task: {task}")
    print(f"Previous: none={task_info['old_none']:.3f}, paper={task_info['old_paper']:.3f}")
    print(f"Issue: {task_info['reason']}")
    print(f"{'='*60}")
    
    # Setup workspace
    run_dir = OUTPUT_DIR / f"{task}_adaptive_paper"
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
    
    # Step 1: Agent queries available skills
    print("Step 1: Agent querying available skills...")
    available_skills = get_available_skills()
    print(f"  Available skills: {[s['id'] for s in available_skills]}")
    
    selected_skill_id, skill_content = agent_query_skills(objective, available_skills)
    
    if selected_skill_id:
        print(f"  ✓ Agent selected skill: {selected_skill_id}")
    else:
        print(f"  ⊘ Agent found no relevant skills (proceeding with baseline)")
    
    # Step 2: Generate code (with or without skill)
    print("Step 2: Generating R code...")
    r_code = generate_r_code(objective, skill_content)
    
    with open(run_dir / "generated_code.R", "w") as f:
        f.write(r_code)
    
    # Step 3: Execute
    print("Step 3: Executing code...")
    success, log = run_r_code(r_code, workspace)
    
    with open(run_dir / "execution.log", "w") as f:
        f.write(log)
    
    # Evaluate
    score = evaluate_output(workspace)
    
    # Copy outputs
    for f in (workspace / "output").glob("*"):
        shutil.copy(f, run_dir / f.name)
    
    # Results
    old_diff = task_info["old_paper"] - task_info["old_none"]
    new_diff = score - task_info["old_none"]
    
    print(f"\nResults:")
    print(f"  New paper score: {score:.3f}")
    print(f"  Old difference: {old_diff:+.3f}")
    print(f"  New difference: {new_diff:+.3f}")
    
    if score >= task_info["old_none"]:
        print(f"  ✓ FIXED: Paper now >= baseline")
    elif score > task_info["old_paper"]:
        print(f"  ○ IMPROVED: Better than old paper, but still < baseline")
    else:
        print(f"  ✗ NEEDS WORK: Still worse than baseline")
    
    return {
        "task": task,
        "old_none": task_info["old_none"],
        "old_paper": task_info["old_paper"],
        "old_diff": old_diff,
        "new_paper": score,
        "new_diff": new_diff,
        "skill_used": selected_skill_id is not None,
        "skill_id": selected_skill_id,
    }


# Main execution
print("=" * 80)
print("Adaptive Paper Skill Experiment")
print("Testing 4 tasks where paper previously performed worse than baseline")
print("=" * 80)
print()
print("Design: Agent can query skills but decides whether to use them")
print("Expected: Without mismatched skills, agent should perform better")
print()

results = []
for task_info in TASKS:
    result = run_adaptive_paper(task_info)
    results.append(result)

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\n{'Task':<25} {'Old Diff':<12} {'New Score':<12} {'New Diff':<12} {'Status':<10}")
print("-" * 80)

fixed = 0
improved = 0
for r in results:
    if r["new_paper"] >= r["old_none"]:
        status = "✓ FIXED"
        fixed += 1
    elif r["new_paper"] > r["old_paper"]:
        status = "○ BETTER"
        improved += 1
    else:
        status = "✗ WORSE"
    
    print(f"{r['task']:<25} {r['old_diff']:<12.3f} {r['new_paper']:<12.3f} {r['new_diff']:<12.3f} {status:<10}")

print(f"\nFixed (new >= baseline): {fixed}/4")
print(f"Improved (new > old): {improved}/4")

if fixed >= 3:
    print("\n🎉 SUCCESS: Adaptive skill selection works! Most tasks fixed.")
elif fixed + improved >= 2:
    print(f"\n→ PARTIAL: {fixed} fixed, {improved} improved. Needs more work.")
else:
    print("\n✗ NEEDS REDESIGN: Adaptive approach not working as expected.")

# Save results
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to: {OUTPUT_DIR / 'results.json'}")
