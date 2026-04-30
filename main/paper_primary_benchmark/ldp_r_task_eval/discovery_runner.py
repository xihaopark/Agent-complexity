#!/usr/bin/env python3
"""Discovery Mode Runner - Paper Arm with agent-autonomous skill retrieval.

This runner enables agents to actively discover and select skills,
rather than having skills pre-bound to tasks.

Usage:
    python discovery_runner.py \
        --registry r_tasks/registry.paper_sensitive_v1.json \
        --config config/paper_discovery_mode.yaml \
        --run-id paper_discovery_20260501
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

# Add paths
_PAPER_PB = Path(__file__).resolve().parent.parent
_MAIN = _PAPER_PB.parent
_REPO_ROOT = _MAIN.parent
if str(_MAIN) not in sys.path:
    sys.path.insert(0, str(_MAIN))

# Import discovery tools
sys.path.insert(0, str(_REPO_ROOT / "paperskills" / "library"))
from discovery_tool import (
    DISCOVERY_TOOLS,
    discover_skills_by_scenario,
    discover_skills_by_criteria,
    get_skill_details,
    find_alternative_tools,
)

from paper_primary_benchmark.ldp_r_task_eval.llm_env import (
    apply_openrouter_key_from_file,
)
from paper_primary_benchmark.ldp_r_task_eval.rollout import (
    save_run_artifacts,
    vanilla_r_task_rollout,
)
from paper_primary_benchmark.ldp_r_task_eval.r_task_env import RTaskEvalEnv

logger = logging.getLogger(__name__)


class DiscoveryRTaskEvalEnv(RTaskEvalEnv):
    """Extended RTaskEvalEnv with discovery tools."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add discovery tools
        from aviary.core import Tool
        self.tools.extend([
            Tool.from_function(self.discover_skills_by_scenario),
            Tool.from_function(self.discover_skills_by_criteria),
            Tool.from_function(self.get_skill_details),
            Tool.from_function(self.find_alternative_tools),
        ])
        self.discovery_call_count = 0
        self.max_discovery_calls = 5
    
    def _check_discovery_limit(self) -> bool:
        """Check if discovery calls within limit."""
        if self.discovery_call_count >= self.max_discovery_calls:
            return False
        self.discovery_call_count += 1
        return True
    
    async def discover_skills_by_scenario(self, scenario: str) -> str:
        """Tool: Discover skills for a scenario."""
        if not self._check_discovery_limit():
            return json.dumps({"error": "Discovery call limit reached"})
        
        result = discover_skills_by_scenario(scenario)
        self.state.actions.append(f"discover:scenario:{scenario}")
        return result
    
    async def discover_skills_by_criteria(
        self,
        analysis_type: str | None = None,
        data_type: str | None = None,
        experimental_design: str | None = None,
    ) -> str:
        """Tool: Discover by criteria."""
        if not self._check_discovery_limit():
            return json.dumps({"error": "Discovery call limit reached"})
        
        result = discover_skills_by_criteria(analysis_type, data_type, experimental_design)
        self.state.actions.append(f"discover:criteria:{analysis_type}:{data_type}:{experimental_design}")
        return result
    
    async def get_skill_details(self, tool_name: str) -> str:
        """Tool: Get detailed skill info."""
        if not self._check_discovery_limit():
            return json.dumps({"error": "Discovery call limit reached"})
        
        result = get_skill_details(tool_name)
        self.state.actions.append(f"discover:details:{tool_name}")
        return result
    
    async def find_alternative_tools(self, tool_name: str) -> str:
        """Tool: Find alternatives."""
        if not self._check_discovery_limit():
            return json.dumps({"error": "Discovery call limit reached"})
        
        result = find_alternative_tools(tool_name)
        self.state.actions.append(f"discover:alternatives:{tool_name}")
        return result


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_registry(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _resolve_work_dir(entry: dict[str, Any]) -> Path:
    rel = entry["work_dir"]
    p = Path(rel)
    if p.is_absolute():
        return p.resolve()
    return (_PAPER_PB / "ldp_r_task_eval" / p).resolve()


async def run_discovery_mode_task(
    task_entry: dict[str, Any],
    config: dict[str, Any],
    run_id: str,
    output_root: Path,
) -> dict[str, Any]:
    """Run single task in discovery mode."""
    
    task_id = task_entry["id"]
    work_dir = _resolve_work_dir(task_entry)
    success_glob = task_entry.get("success_artifact_glob", "output/result.txt")
    
    logger.info(f"[Discovery Mode] Starting {task_id}")
    
    # Create environment with discovery tools
    env = DiscoveryRTaskEvalEnv(
        task_id=task_id,
        work_dir=work_dir,
        objective_file=work_dir / "OBJECTIVE.md",
        success_artifact_glob=success_glob,
        max_steps_soft_trunc=config.get("max_steps", 15),
    )
    
    # Configure agent
    agent_config = config.get("agent", {})
    sys_prompt_template = agent_config.get("sys_prompt", "")
    
    # Discovery mode: NO skill injection, only guidance
    # The prompt already contains discovery tool descriptions
    sys_prompt = sys_prompt_template
    
    # Initialize agent
    from ldp.agent.simple_agent import SimpleAgent
    agent = SimpleAgent(
        llm_model=agent_config.get("llm_model", {"name": "openrouter/openai/gpt-4o"}),
        sys_prompt=sys_prompt,
    )
    
    # Run rollout
    trajectory = await vanilla_r_task_rollout(
        env=env,
        agent=agent,
        max_steps=config.get("max_steps", 15),
    )
    
    # Save artifacts
    task_output_dir = output_root / run_id / task_id
    metadata = save_run_artifacts(
        task_id=task_id,
        run_id=run_id,
        trajectory=trajectory,
        output_dir=task_output_dir,
        git_sha="unknown",
    )
    
    # Add discovery-specific metadata
    metadata["discovery_mode"] = True
    metadata["discovery_calls"] = env.discovery_call_count
    metadata["discovery_actions"] = [a for a in env.state.actions if a.startswith("discover:")]
    
    logger.info(f"[Discovery Mode] Finished {task_id}: {len(metadata['discovery_actions'])} discovery calls")
    
    return metadata


async def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--registry", required=True, type=Path, help="Registry JSON path")
    ap.add_argument("--config", required=True, type=Path, help="Config YAML path")
    ap.add_argument("--run-id", required=True, help="Run identifier")
    ap.add_argument("--output-root", type=Path, default=_PAPER_PB / "ldp_r_task_eval" / "runs")
    ap.add_argument("--openrouter-key-file", type=Path, default=_REPO_ROOT / "openrouterkey.txt")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    
    # Load config and registry
    config = _load_yaml(args.config)
    registry = _load_registry(args.registry)
    
    logger.info(f"Discovery Mode Runner")
    logger.info(f"Registry: {args.registry} ({len(registry.get('tasks', []))} tasks)")
    logger.info(f"Config: {args.config}")
    logger.info(f"Run ID: {args.run_id}")
    
    # Set API key
    if args.openrouter_key_file.exists():
        apply_openrouter_key_from_file(args.openrouter_key_file)
    
    # Run all tasks
    tasks = registry.get("tasks", [])
    results = []
    
    for task_entry in tasks:
        try:
            result = await run_discovery_mode_task(
                task_entry=task_entry,
                config=config,
                run_id=args.run_id,
                output_root=args.output_root,
            )
            results.append(result)
        except Exception as e:
            logger.error(f"Task {task_entry.get('id')} failed: {e}")
            results.append({
                "task_id": task_entry.get("id"),
                "error": str(e),
                "discovery_mode": True,
            })
    
    # Summary
    logger.info(f"\n=== Discovery Mode Summary ===")
    logger.info(f"Total tasks: {len(tasks)}")
    logger.info(f"Completed: {len([r for r in results if 'error' not in r])}")
    total_discovery = sum(r.get("discovery_calls", 0) for r in results)
    logger.info(f"Total discovery calls: {total_discovery}")
    logger.info(f"Avg discovery calls per task: {total_discovery / len(tasks):.1f}")
    
    # Save summary
    summary_path = args.output_root / args.run_id / "discovery_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump({
            "run_id": args.run_id,
            "mode": "discovery",
            "registry": str(args.registry),
            "config": str(args.config),
            "results": results,
        }, f, indent=2)
    
    logger.info(f"Summary saved: {summary_path}")


if __name__ == "__main__":
    asyncio.run(main())
