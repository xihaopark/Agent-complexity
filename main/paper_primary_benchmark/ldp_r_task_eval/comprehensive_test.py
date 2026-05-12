#!/usr/bin/env python3
"""Comprehensive Test - Compare Binding Mode vs Discovery Mode

Runs both Paper Arm variants on the same set of tasks and generates comparison report.

Usage:
    cd main/paper_primary_benchmark/ldp_r_task_eval
    source .venv-ldp-r-task/bin/activate
    python comprehensive_test.py [--tasks 5] [--dry-run]
"""

import argparse
import asyncio
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

_PAPER_PB = Path(__file__).resolve().parent.parent
_LDP = _PAPER_PB / "ldp_r_task_eval"
_REPO_ROOT = _PAPER_PB.parent.parent


def run_command(cmd: list[str], cwd: Path, timeout: int = 600) -> tuple[int, str, str]:
    """Run shell command and return (exit_code, stdout, stderr)."""
    logger.info(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out after {timeout}s")
        return -1, "", "Timeout"


def run_binding_mode(
    registry: Path,
    run_id: str,
    max_tasks: int | None = None,
) -> dict[str, Any]:
    """Run binding mode experiment."""
    logger.info(f"\n{'='*60}")
    logger.info("BINDING MODE - Starting")
    logger.info(f"{'='*60}")
    
    cmd = [
        sys.executable,
        "batch_runner.py",
        "--registry", str(registry),
        "--config", "config/paper_sweep_15steps.yaml",
        "--skill-source", "paper",
        "--run-id", run_id,
    ]
    
    # Note: batch_runner doesn't have a --max-tasks flag
    # We'll filter the registry instead
    
    exit_code, stdout, stderr = run_command(cmd, _LDP, timeout=1800)
    
    # Parse results from runs directory
    output_dir = _LDP / "runs" / run_id
    results = _parse_run_results(output_dir)
    
    return {
        "mode": "binding",
        "run_id": run_id,
        "exit_code": exit_code,
        "results": results,
        "output_dir": str(output_dir),
    }


def run_discovery_mode(
    registry: Path,
    run_id: str,
    max_tasks: int | None = None,
) -> dict[str, Any]:
    """Run discovery mode experiment."""
    logger.info(f"\n{'='*60}")
    logger.info("DISCOVERY MODE - Starting")
    logger.info(f"{'='*60}")
    
    cmd = [
        sys.executable,
        "discovery_runner.py",
        "--registry", str(registry),
        "--config", "config/paper_discovery_mode.yaml",
        "--run-id", run_id,
    ]
    
    exit_code, stdout, stderr = run_command(cmd, _LDP, timeout=1800)
    
    # Parse results
    output_dir = _LDP / "runs" / run_id
    results = _parse_run_results(output_dir)
    
    return {
        "mode": "discovery",
        "run_id": run_id,
        "exit_code": exit_code,
        "results": results,
        "output_dir": str(output_dir),
    }


def _parse_run_results(output_dir: Path) -> list[dict]:
    """Parse results from run output directory."""
    results = []
    
    if not output_dir.exists():
        logger.warning(f"Output directory not found: {output_dir}")
        return results
    
    # Look for task directories
    for task_dir in output_dir.iterdir():
        if not task_dir.is_dir():
            continue
        
        metadata_file = task_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    metadata = json.load(f)
                results.append({
                    "task_id": metadata.get("task_id", task_dir.name),
                    "success": metadata.get("success", False),
                    "steps": metadata.get("steps", 0),
                    "discovery_calls": metadata.get("discovery_calls", 0),
                    "discovery_actions": metadata.get("discovery_actions", []),
                })
            except Exception as e:
                logger.error(f"Failed to parse {metadata_file}: {e}")
    
    return results


def generate_comparison_report(
    binding_results: dict,
    discovery_results: dict,
    output_path: Path,
) -> None:
    """Generate comparison report."""
    
    report = {
        "test_date": datetime.now().isoformat(),
        "binding_mode": {
            "run_id": binding_results["run_id"],
            "total_tasks": len(binding_results["results"]),
            "successful": sum(1 for r in binding_results["results"] if r.get("success")),
            "avg_steps": sum(r.get("steps", 0) for r in binding_results["results"]) / max(len(binding_results["results"]), 1),
        },
        "discovery_mode": {
            "run_id": discovery_results["run_id"],
            "total_tasks": len(discovery_results["results"]),
            "successful": sum(1 for r in discovery_results["results"] if r.get("success")),
            "avg_steps": sum(r.get("steps", 0) for r in discovery_results["results"]) / max(len(discovery_results["results"]), 1),
            "avg_discovery_calls": sum(r.get("discovery_calls", 0) for r in discovery_results["results"]) / max(len(discovery_results["results"]), 1),
        },
        "per_task_comparison": [],
    }
    
    # Per-task comparison
    binding_by_task = {r["task_id"]: r for r in binding_results["results"]}
    discovery_by_task = {r["task_id"]: r for r in discovery_results["results"]}
    
    all_tasks = set(binding_by_task.keys()) | set(discovery_by_task.keys())
    
    for task_id in sorted(all_tasks):
        b = binding_by_task.get(task_id, {})
        d = discovery_by_task.get(task_id, {})
        
        report["per_task_comparison"].append({
            "task_id": task_id,
            "binding": {
                "success": b.get("success", False),
                "steps": b.get("steps", 0),
            },
            "discovery": {
                "success": d.get("success", False),
                "steps": d.get("steps", 0),
                "discovery_calls": d.get("discovery_calls", 0),
            },
        })
    
    # Write report
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info("COMPARISON SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Binding Mode:   {report['binding_mode']['successful']}/{report['binding_mode']['total_tasks']} tasks")
    logger.info(f"Discovery Mode: {report['discovery_mode']['successful']}/{report['discovery_mode']['total_tasks']} tasks")
    logger.info(f"Avg Discovery Calls: {report['discovery_mode']['avg_discovery_calls']:.1f}")
    logger.info(f"Report saved: {output_path}")


def create_mini_registry(num_tasks: int = 2) -> Path:
    """Create a mini registry for quick testing."""
    registry_path = _LDP / "r_tasks" / "registry.test_verified.json"
    
    with open(registry_path) as f:
        reg = json.load(f)
    
    # Take first N tasks
    mini_reg = {
        "version": "mini",
        "kind": "mini_test",
        "description": f"Mini test with {num_tasks} verified tasks",
        "tasks": reg["tasks"][:num_tasks],
    }
    
    mini_path = _LDP / "r_tasks" / f"registry.mini_{num_tasks}.json"
    with open(mini_path, "w") as f:
        json.dump(mini_reg, f, indent=2)
    
    logger.info(f"Created mini registry: {mini_path} ({num_tasks} tasks)")
    return mini_path


async def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tasks", type=int, default=5, help="Number of tasks to test (default: all 5 verified)")
    ap.add_argument("--dry-run", action="store_true", help="Setup check only, don't run experiments")
    args = ap.parse_args()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    logger.info("="*60)
    logger.info("COMPREHENSIVE TEST: Binding vs Discovery Mode")
    logger.info("="*60)
    
    # Check environment
    logger.info("\n[1/4] Environment Check...")
    venv_python = _LDP / ".venv-ldp-r-task" / "bin" / "python3"
    if not venv_python.exists():
        logger.error(f"Virtual environment not found: {venv_python}")
        logger.error("Please run: cd main/paper_primary_benchmark/ldp_r_task_eval && source .venv-ldp-r-task/bin/activate")
        return 1
    logger.info(f"✓ Virtual environment found: {venv_python}")
    
    # Check OpenRouter key
    key_file = _REPO_ROOT / "openrouterkey.txt"
    if not key_file.exists():
        logger.warning(f"⚠ OpenRouter key file not found: {key_file}")
        logger.warning("Experiments will fail without API key")
    else:
        logger.info(f"✓ API key file found: {key_file}")
    
    if args.dry_run:
        logger.info("\n✓ Dry run complete - all checks passed")
        return 0
    
    # Create registry
    logger.info("\n[2/4] Creating test registry...")
    if args.tasks < 5:
        registry = create_mini_registry(args.tasks)
    else:
        registry = _LDP / "r_tasks" / "registry.test_verified.json"
        if not registry.exists():
            logger.error(f"Registry not found: {registry}")
            return 1
    
    logger.info(f"✓ Using registry: {registry}")
    
    # Run experiments
    logger.info("\n[3/4] Running experiments...")
    
    binding_run_id = f"test_binding_{timestamp}"
    discovery_run_id = f"test_discovery_{timestamp}"
    
    # Run binding mode
    logger.info("\n>>> Starting Binding Mode...")
    binding_results = run_binding_mode(registry, binding_run_id)
    
    # Run discovery mode
    logger.info("\n>>> Starting Discovery Mode...")
    discovery_results = run_discovery_mode(registry, discovery_run_id)
    
    # Generate report
    logger.info("\n[4/4] Generating report...")
    report_path = _LDP / "runs" / f"comparison_report_{timestamp}.json"
    generate_comparison_report(binding_results, discovery_results, report_path)
    
    logger.info("\n" + "="*60)
    logger.info("TEST COMPLETE")
    logger.info("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
