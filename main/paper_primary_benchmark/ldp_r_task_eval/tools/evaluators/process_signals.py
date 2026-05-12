"""Parse an ldp trajectory to collect the four V2 process signals.

The four booleans we score:

* ``tool_calls_executed_meaningful`` - >2 non-trivial (non ``list_workdir``) calls
* ``rscript_invoked_and_exited_zero`` - at least one ``run_rscript`` exited 0
* ``submit_done_called`` - trajectory ever calls ``submit_done``
* ``outputs_dir_nonempty_and_valid`` - ``workspace/output`` has a non-empty file

Each signal is 0.0 or 1.0; the ``mean`` is the process score.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


_RUN_RSCRIPT_OK_RE = re.compile(r"(?i)(^|\s)exit(_code)?\s*[=:]\s*0(\b|$)")
_RUN_RSCRIPT_ERR_RE = re.compile(
    r"(?i)(Execution halted|^Error\s|\nError\s|traceback:)",
    re.MULTILINE,
)

_TRIVIAL_TOOLS = {"list_workdir", "read_workdir", "read_plan"}


def _iter_steps(trajectory_path: Path):
    """Yield parsed step dicts, skipping the run-id header line."""
    try:
        with trajectory_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if not isinstance(obj, dict):
                    continue
                yield obj
    except FileNotFoundError:
        return


def _iter_tool_calls(step: dict):
    """Yield (tool_name, args_obj) for each assistant tool_call in a step."""
    action = step.get("action") or {}
    value = action.get("value") if isinstance(action, dict) else None
    if not isinstance(value, dict):
        return
    for call in value.get("tool_calls") or []:
        fn = (call or {}).get("function") or {}
        name = fn.get("name")
        raw_args = fn.get("arguments")
        args: dict = {}
        if isinstance(raw_args, str):
            try:
                args = json.loads(raw_args)
            except Exception:
                args = {}
        elif isinstance(raw_args, dict):
            args = raw_args
        if name:
            yield name, args


def _iter_tool_observations(step: dict):
    """Yield (tool_name, observation_text) pairs from the step's response."""
    for key in ("next_observation", "observation"):
        obs = step.get(key) or []
        if not isinstance(obs, list):
            continue
        for item in obs:
            if isinstance(item, dict) and item.get("role") == "tool":
                yield item.get("name"), str(item.get("content") or "")


def _outputs_dir_nonempty(output_dir: Path) -> bool:
    if not output_dir.is_dir():
        return False
    for p in output_dir.rglob("*"):
        if p.is_file() and p.stat().st_size > 0:
            return True
    return False


def _trajectory_error(trajectory_path: Path, metadata: dict) -> bool:
    """Heuristic: did the run end with an exception before producing output?"""
    status = str(metadata.get("status") or "").lower()
    if status in {"error", "crashed", "exception"}:
        return True
    last: dict | None = None
    for step in _iter_steps(trajectory_path):
        last = step
    if last is None:
        return True
    done = bool(last.get("done"))
    truncated = bool(last.get("truncated"))
    reward = last.get("reward")
    if not done and not truncated and (reward is None or reward == 0):
        obs_chunks = [c for _, c in _iter_tool_observations(last)]
        joined = "\n".join(obs_chunks).lower()
        if "traceback" in joined or "exception" in joined:
            return True
    return False


def extract_process_signals(run_dir: Path, output_dir: Path) -> dict:
    """Return all four signals plus auxiliary counts used by the report."""
    trajectory_path = run_dir / "trajectory.jsonl"
    meta_path = run_dir / "metadata.json"
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}
    except Exception:
        meta = {}

    tool_call_names: list[str] = []
    rscript_ok = 0
    rscript_err = 0
    submit_done = False

    for step in _iter_steps(trajectory_path):
        for name, _args in _iter_tool_calls(step):
            tool_call_names.append(name)
            if name == "submit_done":
                submit_done = True
        for tool_name, content in _iter_tool_observations(step):
            if tool_name == "run_rscript" or (tool_name == "run_shell" and "rscript" in content.lower()[:256]):
                looks_err = bool(_RUN_RSCRIPT_ERR_RE.search(content))
                looks_ok = bool(_RUN_RSCRIPT_OK_RE.search(content))
                if looks_ok and not looks_err:
                    rscript_ok += 1
                elif looks_err:
                    rscript_err += 1
                elif tool_name == "run_rscript" and "Error" not in content:
                    rscript_ok += 1

    meaningful_calls = [n for n in tool_call_names if n not in _TRIVIAL_TOOLS]

    signals = {
        "tool_calls_executed_meaningful": 1.0 if len(meaningful_calls) > 2 else 0.0,
        "rscript_invoked_and_exited_zero": 1.0 if rscript_ok >= 1 else 0.0,
        "submit_done_called": 1.0 if submit_done else 0.0,
        "outputs_dir_nonempty_and_valid": 1.0 if _outputs_dir_nonempty(output_dir) else 0.0,
    }
    mean = sum(signals.values()) / len(signals)
    trajectory_errored = _trajectory_error(trajectory_path, meta)
    return {
        "signals": signals,
        "mean": mean,
        "counts": {
            "tool_calls_total": len(tool_call_names),
            "tool_calls_meaningful": len(meaningful_calls),
            "rscript_ok": rscript_ok,
            "rscript_err": rscript_err,
        },
        "trajectory_errored": trajectory_errored,
    }
