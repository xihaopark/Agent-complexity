from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FINISH_ROOT = ROOT.parent
DEFAULT_WORKFLOW_ID = "rna-seq-star-deseq2-finish"
OBSERVED_OUTPUT_ROOTS = {
    "logs",
    "manifests",
    "output",
    "reports",
    "results",
}
TEXT_PREVIEW_SUFFIXES = {
    ".csv",
    ".html",
    ".json",
    ".log",
    ".md",
    ".svg",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
_EVALUABILITY_INDEX: dict[str, dict[str, Any]] | None = None

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(ROOT / ".env")

from renzo.app.runtime_env import build_runtime_env, find_conda_bin
from renzo.app.workflow_failures import classify_workflow_failure

os.environ.update(build_runtime_env())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return {"status": "failed", "error": "empty json file", "path": str(path)}
        return json.loads(text)
    except Exception as e:
        return {"status": "failed", "error": f"invalid json: {e}", "path": str(path)}


def write_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def link_or_copy_file(src: str, dst: str) -> str:
    dst_path = Path(dst)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    return dst


def resolve_renzo_python(explicit: str | None = None) -> str:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env_candidate = os.environ.get("RENZO_PYTHON", "").strip()
    if env_candidate:
        candidates.append(Path(env_candidate).expanduser())
    candidates.extend(
        [
            ROOT / ".venv312" / "bin" / "python",
            ROOT / ".venv" / "bin" / "python",
        ]
    )
    for candidate in candidates:
        selected = candidate if candidate.is_absolute() else (Path.cwd() / candidate)
        if selected.exists():
            return str(selected)
    return sys.executable


def truncate_text(text: str | None, limit: int = 200_000) -> dict[str, Any]:
    value = text or ""
    return {
        "text": value[:limit],
        "truncated": len(value) > limit,
        "original_length": len(value),
    }


def trace_tail(entries: Any, max_items: int = 3) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        return []
    tail: list[dict[str, Any]] = []
    for raw in entries[-max_items:]:
        if not isinstance(raw, dict):
            continue
        tail.append(
            {
                "trace_id": raw.get("trace_id", ""),
                "at": raw.get("at", ""),
                "event_type": raw.get("event_type", ""),
                "node": raw.get("node", ""),
                "purpose": raw.get("purpose", ""),
                "status": raw.get("status", ""),
                "step_id": raw.get("step_id", ""),
                "reason": str(raw.get("reason", ""))[:1000],
                "response_text": str(((raw.get("response") or {}).get("text") or ""))[:1500],
            }
        )
    return tail


def _as_int(value: Any) -> int | None:
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _nested(mapping: Any, *path: str) -> Any:
    current = mapping
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def llm_entry_step_id(entry: dict[str, Any]) -> str:
    value = entry.get("step_id")
    if isinstance(value, str) and value.strip():
        return value.strip()
    purpose = str(entry.get("purpose") or "")
    if purpose == "select_workflow_step":
        parsed = entry.get("parsed_output")
        if isinstance(parsed, dict):
            value = parsed.get("selected_step_id")
            if isinstance(value, str) and value.strip():
                return value.strip()
        response_text = str(((entry.get("response") or {}).get("text")) or "").strip()
        if response_text:
            candidate = response_text.splitlines()[0].strip().strip('"').strip("'")
            if candidate:
                return candidate
    context = entry.get("context")
    if isinstance(context, dict):
        for key in ("step_id", "current_step_id", "workflow_step_id"):
            value = context.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        workflow_ctx = context.get("workflow_run_context")
        if isinstance(workflow_ctx, dict):
            value = workflow_ctx.get("current_step_id")
            if isinstance(value, str) and value.strip():
                return value.strip()
    return ""


def normalize_token_usage(raw: Any, response_payload: Any = None) -> dict[str, Any]:
    prompt_tokens = (
        _as_int(_nested(raw, "prompt_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "token_usage", "prompt_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "usage", "prompt_tokens"))
        or _as_int(_nested(response_payload, "usage_metadata", "input_tokens"))
        or _as_int(_nested(response_payload, "usage_metadata", "prompt_tokens"))
    )
    completion_tokens = (
        _as_int(_nested(raw, "completion_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "token_usage", "completion_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "usage", "completion_tokens"))
        or _as_int(_nested(response_payload, "usage_metadata", "output_tokens"))
        or _as_int(_nested(response_payload, "usage_metadata", "completion_tokens"))
    )
    total_tokens = (
        _as_int(_nested(raw, "total_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "token_usage", "total_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "usage", "total_tokens"))
        or _as_int(_nested(response_payload, "usage_metadata", "total_tokens"))
    )
    reasoning_tokens = (
        _as_int(_nested(raw, "reasoning_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "token_usage", "completion_tokens_details", "reasoning_tokens"))
        or _as_int(_nested(response_payload, "response_metadata", "token_usage", "output_token_details", "reasoning"))
        or _as_int(_nested(response_payload, "response_metadata", "usage", "completion_tokens_details", "reasoning_tokens"))
        or _as_int(_nested(response_payload, "usage_metadata", "output_token_details", "reasoning"))
    )
    cost = (
        _as_float(_nested(raw, "cost"))
        or _as_float(_nested(response_payload, "response_metadata", "token_usage", "cost"))
        or _as_float(_nested(response_payload, "response_metadata", "usage", "cost"))
        or _as_float(_nested(response_payload, "response_metadata", "cost"))
        or _as_float(_nested(response_payload, "usage_metadata", "cost"))
    )
    payload = {
        "prompt_tokens": prompt_tokens or 0,
        "completion_tokens": completion_tokens or 0,
        "total_tokens": total_tokens or 0,
        "reasoning_tokens": reasoning_tokens or 0,
        "cost": round(cost or 0.0, 7),
    }
    payload["recorded"] = any(payload[key] for key in ("prompt_tokens", "completion_tokens", "total_tokens", "reasoning_tokens")) or payload["cost"] > 0
    return payload


def aggregate_llm_usage(entries: Any) -> dict[str, Any]:
    summary = {
        "llm_call_count": 0,
        "token_recorded_call_count": 0,
        "cost_recorded_call_count": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "reasoning_tokens": 0,
        "cost": 0.0,
        "by_node": {},
        "by_step": {},
    }
    if not isinstance(entries, list):
        return summary
    for raw in entries:
        if not isinstance(raw, dict):
            continue
        usage = normalize_token_usage(raw.get("token_usage"), raw.get("response"))
        summary["llm_call_count"] += 1
        if usage["recorded"]:
            summary["token_recorded_call_count"] += 1
        if usage["cost"] > 0:
            summary["cost_recorded_call_count"] += 1
        for key in ("prompt_tokens", "completion_tokens", "total_tokens", "reasoning_tokens"):
            summary[key] += usage[key]
        summary["cost"] = round(summary["cost"] + usage["cost"], 7)

        node = str(raw.get("node") or "unknown")
        node_summary = summary["by_node"].setdefault(
            node,
            {
                "llm_call_count": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "reasoning_tokens": 0,
                "cost": 0.0,
            },
        )
        node_summary["llm_call_count"] += 1
        for key in ("prompt_tokens", "completion_tokens", "total_tokens", "reasoning_tokens"):
            node_summary[key] += usage[key]
        node_summary["cost"] = round(node_summary["cost"] + usage["cost"], 7)

        step_id = llm_entry_step_id(raw)
        if step_id:
            step_summary = summary["by_step"].setdefault(
                step_id,
                {
                    "llm_call_count": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                    "reasoning_tokens": 0,
                    "cost": 0.0,
                },
            )
            step_summary["llm_call_count"] += 1
            for key in ("prompt_tokens", "completion_tokens", "total_tokens", "reasoning_tokens"):
                step_summary[key] += usage[key]
            step_summary["cost"] = round(step_summary["cost"] + usage["cost"], 7)
    summary["cost"] = round(summary["cost"], 7)
    return summary


def build_direct_step_metrics(manifest: dict[str, Any], step_results: Any) -> list[dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {}
    ordered_ids: list[str] = []
    for index, step in enumerate(manifest.get("steps", []), start=1):
        step_id = str(step.get("id") or f"step-{index}")
        ordered_ids.append(step_id)
        metrics[step_id] = {
            "step_id": step_id,
            "step_name": step.get("name") or step_id,
            "declared_order": index,
            "execution_attempt_count": 0,
            "execution_status": "not_run",
            "duration_seconds_total": 0.0,
            "last_returncode": None,
            "last_failure": {},
        }
    for result in step_results if isinstance(step_results, list) else []:
        if not isinstance(result, dict):
            continue
        step_id = str(result.get("step_id") or "")
        if not step_id:
            continue
        item = metrics.setdefault(
            step_id,
            {
                "step_id": step_id,
                "step_name": step_id,
                "declared_order": len(metrics) + 1,
                "execution_attempt_count": 0,
                "execution_status": "not_run",
                "duration_seconds_total": 0.0,
                "last_returncode": None,
                "last_failure": {},
            },
        )
        item["execution_attempt_count"] += 1
        item["duration_seconds_total"] = round(item["duration_seconds_total"] + float(result.get("duration_seconds") or 0.0), 3)
        item["last_returncode"] = result.get("returncode")
        item["last_failure"] = result.get("failure") or {}
        item["execution_status"] = "success" if result.get("returncode") == 0 else "failed"
        if step_id not in ordered_ids:
            ordered_ids.append(step_id)
    return [metrics[step_id] for step_id in ordered_ids]


def build_agent_step_metrics(
    manifest: dict[str, Any],
    final_state: dict[str, Any],
    turns: Any,
) -> list[dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {}
    ordered_ids: list[str] = []
    for index, step in enumerate(manifest.get("steps", []), start=1):
        step_id = str(step.get("id") or f"step-{index}")
        ordered_ids.append(step_id)
        metrics[step_id] = {
            "step_id": step_id,
            "step_name": step.get("name") or step_id,
            "declared_order": index,
            "plan_status": "pending",
            "turn_count": 0,
            "turn_indices": [],
            "selection_event_count": 0,
            "last_selection_reason": "",
            "llm_call_count": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "reasoning_tokens": 0,
            "cost": 0.0,
            "llm_nodes": [],
            "llm_purposes": [],
            "latest_llm_response_excerpt": "",
            "execution_attempt_count": 0,
            "execution_status": "not_run",
            "duration_seconds_total": 0.0,
            "last_returncode": None,
            "last_failure": {},
        }

    workflow_plan = (final_state.get("workflow_plan") or {})
    for index, step in enumerate(workflow_plan.get("steps") or [], start=1):
        if not isinstance(step, dict):
            continue
        step_id = str(step.get("id") or f"step-{index}")
        item = metrics.setdefault(
            step_id,
            {
                "step_id": step_id,
                "step_name": step.get("name") or step.get("description") or step_id,
                "declared_order": index,
                "plan_status": "pending",
                "turn_count": 0,
                "turn_indices": [],
                "selection_event_count": 0,
                "last_selection_reason": "",
                "llm_call_count": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "reasoning_tokens": 0,
                "cost": 0.0,
                "llm_nodes": [],
                "llm_purposes": [],
                "latest_llm_response_excerpt": "",
                "execution_attempt_count": 0,
                "execution_status": "not_run",
                "duration_seconds_total": 0.0,
                "last_returncode": None,
                "last_failure": {},
            },
        )
        item["step_name"] = step.get("name") or item["step_name"]
        item["plan_status"] = step.get("status") or item["plan_status"]
        if step_id not in ordered_ids:
            ordered_ids.append(step_id)

    for turn in turns if isinstance(turns, list) else []:
        if not isinstance(turn, dict):
            continue
        step_id = str(turn.get("current_step_id") or "")
        if not step_id:
            continue
        item = metrics.setdefault(
            step_id,
            {
                "step_id": step_id,
                "step_name": step_id,
                "declared_order": len(metrics) + 1,
                "plan_status": "pending",
                "turn_count": 0,
                "turn_indices": [],
                "selection_event_count": 0,
                "last_selection_reason": "",
                "llm_call_count": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "reasoning_tokens": 0,
                "cost": 0.0,
                "llm_nodes": [],
                "llm_purposes": [],
                "latest_llm_response_excerpt": "",
                "execution_attempt_count": 0,
                "execution_status": "not_run",
                "duration_seconds_total": 0.0,
                "last_returncode": None,
                "last_failure": {},
            },
        )
        item["turn_count"] += 1
        item["turn_indices"].append(turn.get("turn_index"))
        item["duration_seconds_total"] = round(item["duration_seconds_total"] + float(turn.get("duration_seconds") or 0.0), 3)
        if step_id not in ordered_ids:
            ordered_ids.append(step_id)

    for raw in final_state.get("orchestration_trace") or []:
        if not isinstance(raw, dict):
            continue
        step_id = str(raw.get("step_id") or "")
        if not step_id:
            continue
        item = metrics.setdefault(step_id, {"step_id": step_id, "step_name": step_id, "declared_order": len(metrics) + 1})
        item.setdefault("selection_event_count", 0)
        if raw.get("event_type") == "workflow_step_selected":
            item["selection_event_count"] += 1
            item["last_selection_reason"] = str(raw.get("reason") or "")[:4000]
        if step_id not in ordered_ids:
            ordered_ids.append(step_id)

    for raw in final_state.get("llm_trace") or []:
        if not isinstance(raw, dict):
            continue
        step_id = llm_entry_step_id(raw)
        if not step_id:
            continue
        usage = normalize_token_usage(raw.get("token_usage"), raw.get("response"))
        item = metrics.setdefault(step_id, {"step_id": step_id, "step_name": step_id, "declared_order": len(metrics) + 1})
        for key, default in (
            ("llm_call_count", 0),
            ("prompt_tokens", 0),
            ("completion_tokens", 0),
            ("total_tokens", 0),
            ("reasoning_tokens", 0),
            ("cost", 0.0),
            ("llm_nodes", []),
            ("llm_purposes", []),
            ("latest_llm_response_excerpt", ""),
        ):
            item.setdefault(key, default if not isinstance(default, list) else list(default))
        item["llm_call_count"] += 1
        for key in ("prompt_tokens", "completion_tokens", "total_tokens", "reasoning_tokens"):
            item[key] += usage[key]
        item["cost"] = round(item["cost"] + usage["cost"], 7)
        node = str(raw.get("node") or "unknown")
        purpose = str(raw.get("purpose") or "")
        if node not in item["llm_nodes"]:
            item["llm_nodes"].append(node)
        if purpose and purpose not in item["llm_purposes"]:
            item["llm_purposes"].append(purpose)
        response_text = str(((raw.get("response") or {}).get("text")) or "")
        if response_text:
            item["latest_llm_response_excerpt"] = response_text[:2000]
        if step_id not in ordered_ids:
            ordered_ids.append(step_id)

    for raw in final_state.get("execution_logs") or []:
        if not isinstance(raw, dict):
            continue
        step_id = str(raw.get("step_id") or "")
        if not step_id:
            continue
        item = metrics.setdefault(step_id, {"step_id": step_id, "step_name": step_id, "declared_order": len(metrics) + 1})
        item.setdefault("execution_attempt_count", 0)
        item.setdefault("execution_status", "not_run")
        item.setdefault("duration_seconds_total", 0.0)
        item["execution_attempt_count"] += 1
        item["last_returncode"] = raw.get("returncode")
        metadata = raw.get("metadata") or {}
        item["last_failure"] = metadata.get("failure") if isinstance(metadata, dict) else {}
        returncode = raw.get("returncode")
        if returncode == 0:
            item["execution_status"] = "success"
        elif returncode is not None:
            item["execution_status"] = "failed"
        if step_id not in ordered_ids:
            ordered_ids.append(step_id)

    for item in metrics.values():
        plan_status = str(item.get("plan_status") or "").lower()
        if item.get("execution_status") == "not_run" and plan_status in {"success", "completed"}:
            item["execution_status"] = "success"
        elif item.get("execution_status") == "not_run" and plan_status in {"failed", "error"}:
            item["execution_status"] = "failed"

    output: list[dict[str, Any]] = []
    for step_id in ordered_ids:
        item = metrics[step_id]
        item["cost"] = round(float(item.get("cost") or 0.0), 7)
        output.append(item)
    return output


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_workflow_manifest(workflow_dir: Path) -> dict[str, Any]:
    manifest_path = workflow_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest.json not found in {workflow_dir}")
    return read_json(manifest_path)


def resolve_source_workflow_dir(workflow_id: str) -> Path:
    direct = FINISH_ROOT / workflow_id
    if (direct / "manifest.json").exists():
        return direct
    for manifest_path in FINISH_ROOT.glob("*/manifest.json"):
        data = read_json(manifest_path)
        aliases = set(data.get("aliases") or [])
        aliases.update((data.get("discovery") or {}).get("aliases") or [])
        if workflow_id == data.get("id") or workflow_id in aliases:
            return manifest_path.parent
    raise FileNotFoundError(f"workflow {workflow_id} not found under {FINISH_ROOT}")


def copy_workflow_tree(source_dir: Path, destination_dir: Path) -> Path:
    def rewrite_paths(dest_dir: Path, source_root: str, copied_root: Path) -> None:
        for rel in ["config_basic/config.yaml", "manifest.json", "source-metadata.json"]:
            path = dest_dir / rel
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            new_text = text.replace(source_root, str(copied_root))
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")

    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
    source_meta_path = destination_dir / "source-metadata.json"
    if source_meta_path.exists():
        source_meta = read_json(source_meta_path)
        source_repo_dir = str(source_meta.get("source_repo_dir") or "").strip()
        if source_repo_dir:
            source_repo_path = Path(source_repo_dir).resolve()
            copied_source_root = destination_dir / "source_repo"
            rewrite_paths(destination_dir, source_repo_dir, copied_source_root)
            if source_repo_path.exists() and not copied_source_root.exists():
                copied_source_root.mkdir(parents=True, exist_ok=True)
                skip_names = {".git", ".github", ".snakemake", "__pycache__"}
                for child in source_repo_path.iterdir():
                    if child.name in skip_names:
                        continue
                    dst = copied_source_root / child.name
                    if dst.exists():
                        continue
                    if child.is_dir():
                        shutil.copytree(child, dst, copy_function=link_or_copy_file)
                    elif child.is_file():
                        link_or_copy_file(child, dst)
            rewrite_paths(destination_dir, source_repo_dir, copied_source_root)
    return destination_dir


def rewrite_manifest_step_order(workflow_dir: Path, mode: str) -> None:
    manifest_path = workflow_dir / "manifest.json"
    manifest = read_json(manifest_path)
    steps = list(manifest.get("steps") or [])
    if mode == "reverse":
        manifest["steps"] = list(reversed(steps))
    else:
        raise ValueError(f"Unsupported manifest rewrite mode: {mode}")
    write_json(manifest_path, manifest)


def should_observe_output(relpath: str) -> bool:
    first = relpath.split("/", 1)[0]
    return first in OBSERVED_OUTPUT_ROOTS


def file_record(path: Path, root: Path, include_hash: bool = True) -> dict[str, Any]:
    stat = path.stat()
    relpath = normalize_relpath(path, root)
    record: dict[str, Any] = {
        "path": relpath,
        "size": stat.st_size,
        "mtime": int(stat.st_mtime),
    }
    if include_hash and stat.st_size <= 2 * 1024 * 1024:
        record["sha256"] = sha256_file(path)
    if path.suffix.lower() in TEXT_PREVIEW_SUFFIXES and stat.st_size <= 128 * 1024:
        try:
            record["preview"] = path.read_text(encoding="utf-8", errors="replace")[:4000]
        except Exception:
            record["preview"] = ""
    return record


def collect_observed_outputs(workflow_dir: Path, include_hash: bool = True) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    for path in sorted(workflow_dir.rglob("*")):
        if not path.is_file():
            continue
        relpath = normalize_relpath(path, workflow_dir)
        if not should_observe_output(relpath):
            continue
        outputs.append(file_record(path, workflow_dir, include_hash=include_hash))
    return outputs


def inventory_index(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(item["path"]): item for item in items}


def diff_inventories(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> dict[str, Any]:
    before_index = inventory_index(before)
    after_index = inventory_index(after)
    created = [path for path in after_index if path not in before_index]
    removed = [path for path in before_index if path not in after_index]
    changed = [
        path
        for path in after_index
        if path in before_index
        and (
            after_index[path].get("size") != before_index[path].get("size")
            or after_index[path].get("sha256") != before_index[path].get("sha256")
        )
    ]
    return {
        "created": sorted(created),
        "removed": sorted(removed),
        "changed": sorted(changed),
        "created_count": len(created),
        "removed_count": len(removed),
        "changed_count": len(changed),
    }


def evaluate_declared_outputs(workflow_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    declared: list[str] = []
    for step in manifest.get("steps", []):
        declared.extend(str(item) for item in step.get("outputs", []) if str(item).strip())
    unique_declared = sorted(dict.fromkeys(declared))
    present = [path for path in unique_declared if (workflow_dir / path).exists()]
    missing = [path for path in unique_declared if path not in present]
    return {
        "declared": unique_declared,
        "present": present,
        "missing": missing,
        "present_count": len(present),
        "missing_count": len(missing),
        "coverage": (len(present) / len(unique_declared)) if unique_declared else 1.0,
    }


def state_signature(state: dict[str, Any]) -> str:
    workflow_plan = state.get("workflow_plan") or {}
    steps = workflow_plan.get("steps") or []
    summary = {
        "workflow_status": state.get("workflow_status"),
        "current_step_id": state.get("current_step_id"),
        "plan_status": state.get("plan_status"),
        "steps": [(step.get("id"), step.get("status")) for step in steps],
        "execution_log_count": len(state.get("execution_logs") or []),
        "artifact_count": len(state.get("artifact_index") or []),
    }
    return sha256_text(json.dumps(summary, ensure_ascii=False, sort_keys=True))


def summarize_validation(validation: Any) -> dict[str, Any]:
    if not isinstance(validation, dict):
        return {}
    return {
        "ok": validation.get("ok"),
        "matched_pattern_ids": validation.get("matched_pattern_ids"),
        "stderr_excerpt": (validation.get("stderr_excerpt") or "")[:1000],
        "stdout_excerpt": (validation.get("stdout_excerpt") or "")[:1000],
    }


def summarize_execution_log(log: Any) -> dict[str, Any]:
    if not isinstance(log, dict):
        return {}
    return {
        "command": log.get("command"),
        "returncode": log.get("returncode"),
        "step_id": log.get("step_id"),
        "workflow_id": log.get("workflow_id"),
        "stdout_tail": (log.get("stdout") or "")[-1000:],
        "stderr_tail": (log.get("stderr") or "")[-1000:],
        "failure": log.get("metadata", {}).get("failure") if isinstance(log.get("metadata"), dict) else {},
    }


def summarize_state_snapshot(state: dict[str, Any]) -> dict[str, Any]:
    execution_logs = state.get("execution_logs") or []
    artifacts = state.get("artifact_index") or []
    workflow_plan = state.get("workflow_plan") or {}
    plan_steps = workflow_plan.get("steps") or []
    return {
        "observed_at": now_iso(),
        "workflow_status": state.get("workflow_status"),
        "current_step_id": state.get("current_step_id"),
        "plan_status": state.get("plan_status"),
        "workflow_run_context": state.get("workflow_run_context"),
        "execution_workdir": state.get("execution_workdir"),
        "artifact_count": len(artifacts),
        "execution_log_count": len(execution_logs),
        "last_execution_log": summarize_execution_log(execution_logs[-1]) if execution_logs else {},
        "validation_result": summarize_validation(state.get("validation_result")),
        "llm_call_count": len(state.get("llm_trace") or []),
        "orchestration_event_count": len(state.get("orchestration_trace") or []),
        "llm_usage_summary": aggregate_llm_usage(state.get("llm_trace")),
        "llm_trace_tail": trace_tail(state.get("llm_trace")),
        "orchestration_trace_tail": trace_tail(state.get("orchestration_trace")),
        "step_statuses": [
            {"id": step.get("id"), "status": step.get("status")}
            for step in plan_steps
        ],
        "signature": state_signature(state),
    }


def load_evaluability_index() -> dict[str, dict[str, Any]]:
    global _EVALUABILITY_INDEX
    if _EVALUABILITY_INDEX is not None:
        return _EVALUABILITY_INDEX
    path = FINISH_ROOT / "WORKFLOW_EVALUABILITY_STATUS.json"
    if not path.exists():
        _EVALUABILITY_INDEX = {}
        return _EVALUABILITY_INDEX
    payload = read_json(path)
    _EVALUABILITY_INDEX = {
        str(row.get("workflow_id") or ""): row
        for row in payload.get("workflow_evaluability") or []
        if isinstance(row, dict) and str(row.get("workflow_id") or "").strip()
    }
    return _EVALUABILITY_INDEX


def default_evaluability(workflow_id: str, workflow_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    protocol_ok = bool((workflow_dir / "manifest.json").exists() and list(manifest.get("steps") or []))
    inputs_ready = bool((workflow_dir / "config_basic" / "config.yaml").exists())
    return {
        "workflow_id": workflow_id,
        "workflow_dir": str(workflow_dir),
        "evaluable": bool(protocol_ok and inputs_ready),
        "protocol_ok": protocol_ok,
        "inputs_ready": inputs_ready,
        "env_ready": True,
        "reason": "fallback evaluability derived from local manifest/config presence",
        "evidence": [],
        "noise_flags": [],
        "recommended_bucket": "main_table" if protocol_ok and inputs_ready else "fix_then_retry",
    }


def get_workflow_evaluability(workflow_id: str, workflow_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    return dict(load_evaluability_index().get(workflow_id) or default_evaluability(workflow_id, workflow_dir, manifest))


def find_turn_node_id(turn_nodes: list[dict[str, Any]], step_id: str) -> str:
    if not step_id:
        return "workflow-run"
    for node in turn_nodes:
        if str(node.get("step_id") or "") == step_id:
            return str(node.get("node_id") or "workflow-run")
    return str(turn_nodes[-1].get("node_id") or "workflow-run") if turn_nodes else "workflow-run"


def build_direct_trace_nodes(
    manifest: dict[str, Any],
    step_results: list[dict[str, Any]],
    declared_outputs: dict[str, Any],
    observed_outputs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = [
        {
            "node_id": "workflow-run",
            "parent_id": "",
            "node_type": "workflow_run",
            "stage": "execution",
            "step_id": "",
            "status": "success" if step_results and step_results[-1].get("returncode") == 0 else "failed",
            "started_at": step_results[0].get("started_at") if step_results else "",
            "ended_at": step_results[-1].get("ended_at") if step_results else "",
            "evidence_refs": [],
        }
    ]
    for index, step in enumerate(step_results, start=1):
        step_id = str(step.get("step_id") or f"step-{index}")
        exec_node_id = f"exec-{index}-{step_id}"
        nodes.append(
            {
                "node_id": exec_node_id,
                "parent_id": "workflow-run",
                "node_type": "execution_attempt",
                "stage": "execution",
                "step_id": step_id,
                "status": "success" if step.get("returncode") == 0 else "failed",
                "started_at": step.get("started_at", ""),
                "ended_at": step.get("ended_at", ""),
                "evidence_refs": [f"steps[{index - 1}]"],
                "failure": step.get("failure") or {},
            }
        )
        nodes.append(
            {
                "node_id": f"artifact-{index}-{step_id}",
                "parent_id": exec_node_id,
                "node_type": "artifact_delta",
                "stage": "execution",
                "step_id": step_id,
                "status": "observed",
                "started_at": step.get("started_at", ""),
                "ended_at": step.get("ended_at", ""),
                "evidence_refs": [f"steps[{index - 1}].outputs_delta"],
                "artifact_delta": step.get("outputs_delta") or {},
            }
        )
        nodes.append(
            {
                "node_id": f"validation-{index}-{step_id}",
                "parent_id": exec_node_id,
                "node_type": "validation_event",
                "stage": "validation",
                "step_id": step_id,
                "status": "passed" if step.get("returncode") == 0 else "failed",
                "started_at": step.get("ended_at", ""),
                "ended_at": step.get("ended_at", ""),
                "evidence_refs": [f"steps[{index - 1}].failure"],
            }
        )
    nodes.append(
        {
            "node_id": "artifact-summary",
            "parent_id": "workflow-run",
            "node_type": "artifact_delta",
            "stage": "summary/reporting",
            "step_id": "",
            "status": "observed",
            "started_at": "",
            "ended_at": "",
            "evidence_refs": ["declared_outputs", "observed_outputs"],
            "artifact_summary": {
                "declared_output_present_count": declared_outputs.get("present_count"),
                "declared_output_missing_count": declared_outputs.get("missing_count"),
                "observed_output_count": len(observed_outputs),
            },
        }
    )
    return nodes


def build_agent_trace_nodes(
    turns: list[dict[str, Any]],
    final_state: dict[str, Any],
    declared_outputs: dict[str, Any],
    observed_outputs: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = [
        {
            "node_id": "workflow-run",
            "parent_id": "",
            "node_type": "workflow_run",
            "stage": "summary/reporting",
            "step_id": "",
            "status": str(final_state.get("workflow_status") or "failed"),
            "started_at": turns[0].get("started_at") if turns else "",
            "ended_at": turns[-1].get("ended_at") if turns else "",
            "evidence_refs": [],
        }
    ]
    turn_nodes: list[dict[str, Any]] = []
    for turn in turns:
        turn_index = int(turn.get("turn_index") or 0)
        turn_node_id = f"turn-{turn_index}"
        step_id = str(turn.get("current_step_id") or "")
        turn_node = {
            "node_id": turn_node_id,
            "parent_id": "workflow-run",
            "node_type": "turn",
            "stage": "step_selection",
            "step_id": step_id,
            "status": str(turn.get("workflow_status") or ""),
            "started_at": turn.get("started_at", ""),
            "ended_at": turn.get("ended_at", ""),
            "evidence_refs": [f"turns[{turn_index - 1}]"],
        }
        turn_nodes.append(turn_node)
        nodes.append(turn_node)
        nodes.append(
            {
                "node_id": f"selection-{turn_index}",
                "parent_id": turn_node_id,
                "node_type": "selection_event",
                "stage": "step_selection",
                "step_id": step_id,
                "status": "selected" if step_id else "unknown",
                "started_at": turn.get("started_at", ""),
                "ended_at": turn.get("ended_at", ""),
                "evidence_refs": [f"turns[{turn_index - 1}].llm_trace_delta_tail", f"turns[{turn_index - 1}].orchestration_trace_delta_tail"],
                "reason": str(
                    (
                        ((turn.get("orchestration_trace_delta_tail") or [{}])[-1]).get("reason")
                        or ((turn.get("llm_trace_delta_tail") or [{}])[-1]).get("response_text")
                        or ""
                    )
                )[:2000],
            }
        )
        nodes.append(
            {
                "node_id": f"validation-turn-{turn_index}",
                "parent_id": turn_node_id,
                "node_type": "validation_event",
                "stage": "validation",
                "step_id": step_id,
                "status": str(turn.get("workflow_status") or ""),
                "started_at": turn.get("ended_at", ""),
                "ended_at": turn.get("ended_at", ""),
                "evidence_refs": [f"turns[{turn_index - 1}].trace"],
            }
        )

    for index, raw in enumerate(final_state.get("execution_logs") or [], start=1):
        if not isinstance(raw, dict):
            continue
        step_id = str(raw.get("step_id") or "")
        parent_id = find_turn_node_id(turn_nodes, step_id)
        nodes.append(
            {
                "node_id": f"exec-{index}-{step_id or 'unknown'}",
                "parent_id": parent_id,
                "node_type": "execution_attempt",
                "stage": "execution",
                "step_id": step_id,
                "status": "success" if raw.get("returncode") == 0 else "failed",
                "started_at": raw.get("started_at", ""),
                "ended_at": raw.get("ended_at", ""),
                "evidence_refs": [f"final_state.execution_logs[{index - 1}]"],
                "failure": ((raw.get("metadata") or {}).get("failure") if isinstance(raw.get("metadata"), dict) else {}),
            }
        )

    nodes.append(
        {
            "node_id": "artifact-summary",
            "parent_id": "workflow-run",
            "node_type": "artifact_delta",
            "stage": "summary/reporting",
            "step_id": "",
            "status": "observed",
            "started_at": "",
            "ended_at": "",
            "evidence_refs": ["declared_outputs", "observed_outputs"],
            "artifact_summary": {
                "declared_output_present_count": declared_outputs.get("present_count"),
                "declared_output_missing_count": declared_outputs.get("missing_count"),
                "observed_output_count": len(observed_outputs),
            },
        }
    )
    return nodes, turn_nodes


def stage_summaries_from_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    for node in nodes:
        stage = str(node.get("stage") or "unknown")
        item = summary.setdefault(stage, {"stage": stage, "node_count": 0, "failed_count": 0, "statuses": []})
        item["node_count"] += 1
        status = str(node.get("status") or "")
        if status in {"failed", "error"}:
            item["failed_count"] += 1
        if status and status not in item["statuses"]:
            item["statuses"].append(status)
    return list(summary.values())


def infer_onset_category(
    *,
    evaluability: dict[str, Any],
    failure: dict[str, Any],
    validation_result: dict[str, Any],
    false_success_claim: bool,
) -> tuple[str, str]:
    if not bool(evaluability.get("evaluable")):
        return "workflow_not_evaluable", "input_readiness"
    if false_success_claim:
        return "hallucinated_success_summary", "summary/reporting"
    text = json.dumps(failure or {}, ensure_ascii=False).lower()
    if "missinginput" in text or "missing required path" in text or "missing input" in text:
        return "missing_input_not_detected", "input_readiness"
    if isinstance(validation_result, dict) and validation_result.get("ok") is False:
        return "validation_failure_ignored", "validation"
    return "execution_failure_not_recovered", "execution"


def build_error_chain(
    step_metrics: list[dict[str, Any]],
    onset_step_id: str,
    terminal_symptom: str,
) -> list[dict[str, Any]]:
    chain: list[dict[str, Any]] = []
    if onset_step_id:
        started = False
        for item in step_metrics:
            step_id = str(item.get("step_id") or "")
            if step_id == onset_step_id:
                started = True
            if not started:
                continue
            status = str(item.get("execution_status") or item.get("plan_status") or "")
            if status in {"failed", "not_run", "error"}:
                chain.append(
                    {
                        "step_id": step_id,
                        "status": status,
                        "failure": item.get("last_failure") or {},
                    }
                )
    if terminal_symptom:
        chain.append({"step_id": "", "status": "terminal_symptom", "failure": {"summary": terminal_symptom}})
    return chain[:8]


def diagnostic_replay_hint(failure_onset: dict[str, Any]) -> dict[str, Any]:
    category = str(failure_onset.get("onset_category") or "")
    advice_map = {
        "workflow_not_evaluable": "Do not optimize the agent yet. Fix workflow protocol or missing inputs first.",
        "missing_input_not_detected": "Validate required inputs before selecting downstream steps and stop early if inputs are missing.",
        "execution_failure_not_recovered": "When a subprocess fails, surface the concrete error and avoid repeating the same failing action without a change.",
        "validation_failure_ignored": "Treat validation failures as blocking signals and require recovery before moving on.",
        "hallucinated_success_summary": "Only claim success when declared outputs and validation evidence support it.",
        "wrong_step_selection": "Prefer dependency-respecting ready steps with stronger output grounding.",
    }
    return {
        "allowed_recovery_advice": advice_map.get(category, "Re-evaluate the onset evidence and prefer the safest dependency-respecting recovery action."),
        "failure_onset": {
            "onset_stage": failure_onset.get("onset_stage"),
            "onset_step_id": failure_onset.get("onset_step_id"),
            "onset_category": failure_onset.get("onset_category"),
        },
    }


def annotate_payload(
    payload: dict[str, Any],
    *,
    manifest: dict[str, Any],
    workflow_dir: Path,
) -> dict[str, Any]:
    workflow_id = str(manifest.get("id") or payload.get("workflow_id") or "")
    evaluability = get_workflow_evaluability(workflow_id, workflow_dir, manifest)
    step_metrics = list(payload.get("step_metrics") or [])
    declared_outputs = payload.get("declared_outputs") or {}
    observed_outputs = list(payload.get("observed_outputs") or [])
    validation_result = ((payload.get("final_state") or {}).get("validation_result")) or {}
    false_success_claim = bool(
        payload.get("status") == "success"
        and (
            float(declared_outputs.get("coverage") or 0.0) < 1.0
            or (isinstance(validation_result, dict) and validation_result.get("ok") is False)
        )
    )

    if payload.get("mode") == "direct":
        trace_nodes = build_direct_trace_nodes(manifest, list(payload.get("steps") or []), declared_outputs, observed_outputs)
        turn_summaries: list[dict[str, Any]] = []
    else:
        trace_nodes, turn_nodes = build_agent_trace_nodes(
            list(payload.get("turns") or []),
            payload.get("final_state") or {},
            declared_outputs,
            observed_outputs,
        )
        turn_summaries = turn_nodes

    failed_step = next(
        (
            item for item in step_metrics
            if str(item.get("execution_status") or item.get("plan_status") or "").lower() in {"failed", "error"}
        ),
        None,
    )
    failure = (failed_step or {}).get("last_failure") or {}
    terminal_symptom = ""
    error_chain: list[dict[str, Any]] = []
    if payload.get("status") == "success" and not false_success_claim:
        failure_onset = {
            "onset_stage": "",
            "onset_turn": None,
            "onset_step_id": "",
            "onset_category": "",
            "onset_evidence": "",
            "downstream_chain": [],
            "terminal_symptom": "",
        }
    else:
        onset_category, onset_stage = infer_onset_category(
            evaluability=evaluability,
            failure=failure,
            validation_result=validation_result,
            false_success_claim=false_success_claim,
        )
        onset_step_id = (
            ""
            if onset_category == "workflow_not_evaluable"
            else str((failed_step or {}).get("step_id") or payload.get("current_step_id") or "")
        )
        onset_turn = None
        if onset_step_id:
            for turn in payload.get("turns") or []:
                if str(turn.get("current_step_id") or "") == onset_step_id:
                    onset_turn = turn.get("turn_index")
                    break
        terminal_symptom = str(
            (failure.get("summary") if isinstance(failure, dict) else "")
            or payload.get("workflow_status")
            or payload.get("status")
            or ""
        )
        error_chain = build_error_chain(step_metrics, onset_step_id, terminal_symptom)
        failure_onset = {
            "onset_stage": onset_stage,
            "onset_turn": onset_turn,
            "onset_step_id": onset_step_id,
            "onset_category": onset_category,
            "onset_evidence": (
                str((failure.get("summary") if isinstance(failure, dict) else "") or evaluability.get("reason") or terminal_symptom)[:2000]
            ),
            "downstream_chain": error_chain,
            "terminal_symptom": terminal_symptom,
        }
    trace_tree = {
        "root_id": "workflow-run",
        "node_count": len(trace_nodes),
        "stage_count": len({str(node.get("stage") or "") for node in trace_nodes}),
    }
    payload.update(
        {
            "evaluable": bool(evaluability.get("evaluable")),
            "evaluability": evaluability,
            "failure_onset": failure_onset,
            "error_chain": error_chain,
            "diagnostic_replay_hint": diagnostic_replay_hint(failure_onset),
            "trace_tree": trace_tree,
            "trace_nodes": trace_nodes,
            "turn_summaries": turn_summaries,
            "stage_summaries": stage_summaries_from_nodes(trace_nodes),
            "recovery_attempt_count": sum(1 for item in step_metrics if int(item.get("execution_attempt_count") or 0) > 1),
            "false_success_claim": false_success_claim,
            "summary_faithfulness": {
                "declared_output_coverage": declared_outputs.get("coverage"),
                "status_supported_by_outputs": not false_success_claim,
                "false_success_claim": false_success_claim,
            },
            "workflow_noise_flags": list(evaluability.get("noise_flags") or []),
            "terminal_symptom": terminal_symptom,
        }
    )
    return payload


def serializable_agent_state(state: dict[str, Any], messages: list[dict[str, Any]]) -> dict[str, Any]:
    payload = dict(state)
    payload["messages"] = messages
    return payload


def worker_failure_payload(error: BaseException, *, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "failed",
        "failed_at": now_iso(),
        "error_type": error.__class__.__name__,
        "error": str(error),
        "traceback": traceback.format_exc(),
        "context": context,
    }


def direct_command_for_step(
    workflow_dir: Path,
    step: dict[str, Any],
    *,
    dry_run: bool,
) -> tuple[list[str], Path]:
    params = dict(step.get("params") or {})
    conda_bin = find_conda_bin()
    env_name = str(params.get("shared_conda_env") or os.environ.get("WORKFLOW_SNAKEMAKE_ENV", "snakemake")).strip()
    if conda_bin and env_name:
        command = [conda_bin, "run", "-n", env_name, "python", "-m", "snakemake"]
    else:
        command = [sys.executable, "-m", "snakemake"]
    snakefile = workflow_dir / str(params.get("snakefile") or f"steps/{step['id']}.smk")
    command.extend(["-s", str(snakefile.resolve())])
    run_directory = str(params.get("run_directory") or ".")
    execution_cwd = workflow_dir if run_directory in {".", ""} else (workflow_dir / run_directory).resolve()
    execution_cwd.mkdir(parents=True, exist_ok=True)
    command.extend(["--directory", str(execution_cwd)])
    command.extend(["--cores", str(params.get("cores", 1)), "--printshellcmds"])
    configfile = params.get("configfile")
    if configfile:
        command.extend(["--configfile", str((workflow_dir / str(configfile)).resolve())])
    if params.get("use_conda"):
        command.append("--use-conda")
    extra_args = params.get("extra_args")
    if isinstance(extra_args, list):
        command.extend(str(item) for item in extra_args)
    elif extra_args:
        command.extend(str(extra_args).split())
    targets = [str(target) for target in (step.get("targets") or []) if str(target).strip()]
    if targets and targets != ["all"]:
        command.extend(targets)
    config_items = params.get("config_items") or {}
    for key, value in config_items.items():
        command.extend(["--config", f"{key}={value}"])
    if dry_run:
        command.append("-n")
    return command, execution_cwd


def run_worker_direct(args: argparse.Namespace) -> int:
    workflow_dir = Path(args.workflow_dir).resolve()
    result_json = Path(args.result_json).resolve()
    manifest = load_workflow_manifest(workflow_dir)
    step_results: list[dict[str, Any]] = []
    started_at = now_iso()
    try:
        for step in manifest.get("steps", []):
            step_id = str(step.get("id"))
            # No hashing during intermediate scans to align with agent mode runtime
            before_outputs = collect_observed_outputs(workflow_dir, include_hash=False)
            command, execution_cwd = direct_command_for_step(workflow_dir, step, dry_run=args.dry_run)
            step_started = time.time()
            completed = subprocess.run(
                command,
                cwd=str(execution_cwd),
                capture_output=True,
                text=True,
                timeout=args.timeout_per_step,
                env=build_runtime_env(),
            )
            after_outputs = collect_observed_outputs(workflow_dir, include_hash=False)
            step_results.append(
                {
                    "step_id": step_id,
                    "name": step.get("name"),
                    "command": command,
                    "cwd": str(execution_cwd),
                    "started_at": datetime.fromtimestamp(step_started, tz=timezone.utc).isoformat(),
                    "ended_at": now_iso(),
                    "duration_seconds": round(time.time() - step_started, 3),
                    "returncode": completed.returncode,
                    "stdout": truncate_text(completed.stdout),
                    "stderr": truncate_text(completed.stderr),
                    "outputs_before_count": len(before_outputs),
                    "outputs_after_count": len(after_outputs),
                    "outputs_delta": diff_inventories(before_outputs, after_outputs),
                    "failure": (
                        classify_workflow_failure(
                            completed.stdout,
                            completed.stderr,
                            work_dir=execution_cwd,
                        )
                        if completed.returncode != 0
                        else {}
                    ),
                }
            )
            if completed.returncode != 0:
                break
        # Final observation with hashing for consistency check
        observed_outputs = collect_observed_outputs(workflow_dir, include_hash=True)
        declared_outputs = evaluate_declared_outputs(workflow_dir, manifest)
        step_metrics = build_direct_step_metrics(manifest, step_results)
        success = bool(step_results) and step_results[-1]["returncode"] == 0 and len(step_results) == len(manifest.get("steps", []))
        payload = {
            "mode": "direct",
            "workflow_id": manifest.get("id"),
            "workflow_dir": str(workflow_dir),
            "started_at": started_at,
            "ended_at": now_iso(),
            "status": "success" if success else "failed",
            "step_count": len(manifest.get("steps", [])),
            "completed_step_count": sum(1 for item in step_results if item.get("returncode") == 0),
            "dry_run": bool(args.dry_run),
            "steps": step_results,
            "step_metrics": step_metrics,
            "declared_outputs": declared_outputs,
            "observed_outputs": observed_outputs,
        }
        payload = annotate_payload(payload, manifest=manifest, workflow_dir=workflow_dir)
        write_json(result_json, payload)
        return 0 if success else 1
    except Exception as error:
        write_json(
            result_json,
            worker_failure_payload(
                error,
                context={
                    "mode": "direct",
                    "workflow_dir": str(workflow_dir),
                    "result_json": str(result_json),
                },
            ),
        )
        return 1


def create_agent_session(client: Any, workflow_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    experiment = client.post(
        "/api/experiments",
        json={
            "name": f"Comparison run for {workflow_id}",
            "description": "Direct-vs-agent comparison run",
            "workflow_id": workflow_id,
        },
    ).json()
    session = client.post(
        f"/api/experiments/{experiment['id']}/sessions",
        json={"name": f"comparison-{workflow_id}"},
    ).json()
    return experiment, session


def init_agent_state(
    agent: Any,
    workflow: dict[str, Any],
    experiment: dict[str, Any],
    session: dict[str, Any],
    *,
    strict_manifest: bool,
) -> None:
    agent.state["workflow_id_requested"] = workflow["id"]
    agent.state["experiment_id"] = experiment["id"]
    agent.state["session_id"] = session["id"]
    agent.state["artifact_policy"] = "session"
    agent.state["workflow_run_context"] = {
        "run_id": f"wf-{workflow['id']}-{session['id'][:8]}",
        "workflow_id": workflow["id"],
        "engine": workflow["engine"],
        "experiment_id": experiment["id"],
        "session_id": session["id"],
        "execution_mode": "batch",
        "strict_manifest": strict_manifest,
        "skills_only": True,
        "step_selection": "llm",
        "orchestration_mode": "skills_only",
        "manifest_step_graph_allowed": False,
        "status": "queued",
        "current_step_id": None,
        "started_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "ended_at": None,
        "error_summary": "",
    }


def get_workflow_from_api(client: Any, workflow_id: str) -> dict[str, Any]:
    workflows = client.get("/api/workflows").json().get("workflows", [])
    for workflow in workflows:
        if workflow.get("id") == workflow_id:
            return workflow
    raise RuntimeError(f"workflow {workflow_id} not found from /api/workflows")


def fetch_memory_items(client: Any, experiment_id: str, session_id: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    memory_index = client.get(f"/api/experiments/{experiment_id}/sessions/{session_id}/memory").json()
    manifest = ((memory_index or {}).get("memory_manifest") or {}).get("items") or {}
    for item_id in [
        "artifact_index",
        "execution_logs",
        "plan_steps",
        "qc_results",
        "workflow_plan",
        "workflow_run_context",
    ]:
        if item_id not in manifest:
            continue
        result[item_id] = client.get(
            f"/api/experiments/{experiment_id}/sessions/{session_id}/memory/{item_id}"
        ).json()
    return result


def io_only_initial_prompt(workflow_id: str) -> str:
    return (
        f"Run the linked workflow {workflow_id} from start to finish in IO-only mode. "
        "Use only the workflow-local inputs, declared step IO contracts, and loaded skill documents. "
        "Generate the finish outputs on disk and do not depend on unrelated repository files. "
        "Do not read, reconstruct from, or rely on any manifest DAG or manifest step ordering."
    )


def io_only_continue_prompt(workflow_id: str) -> str:
    return (
        f"Continue the IO-only execution of {workflow_id}. "
        "Keep following the workflow-local IO contracts and the loaded workflow skills, not any manifest DAG."
    )


def run_worker_agent(args: argparse.Namespace) -> int:
    workflow_dir = Path(args.workflow_dir).resolve()
    finish_root = Path(args.finish_root).resolve()
    result_json = Path(args.result_json).resolve()
    data_root = Path(args.data_root).resolve()
    agent_name = str(getattr(args, "agent_name", "") or "renzo").strip() or "renzo"
    manifest = load_workflow_manifest(workflow_dir)
    try:
        conda_bin = find_conda_bin()
        if conda_bin:
            os.environ.setdefault("CONDA_EXE", conda_bin)
        os.environ["WORKFLOW_POOL_DIR"] = str(finish_root)
        os.environ["DATA_ROOT"] = str(data_root)
        os.environ.setdefault("WORKFLOW_SNAKEMAKE_ENV", "snakemake")
        skills_dir = (ROOT.parent.parent / ".trae" / "skills").resolve()
        os.environ["WORKFLOW_SKILLS_DIR"] = str(skills_dir)
        sys.path.insert(0, str(ROOT))
        sys.path.insert(0, str(ROOT / "backend"))
        import api_gateway as api
        from fastapi.testclient import TestClient

        client = TestClient(api.app)
        workflow = get_workflow_from_api(client, manifest["id"])
        experiment, session = create_agent_session(client, manifest["id"])
        agent = api.RenzoAgent(auto_load_skills=False)
        loaded_skill_specs = agent.load_workflow_skills(
            workflow["id"],
            base_dir=str(skills_dir),
            clear_existing=True,
        )
        if not loaded_skill_specs:
            raise RuntimeError(
                f"No standardized skills found for workflow {workflow['id']} in {skills_dir}"
            )
        init_agent_state(
            agent,
            workflow,
            experiment,
            session,
            strict_manifest=bool(args.strict_manifest),
        )

        messages: list[dict[str, Any]] = []
        turns: list[dict[str, Any]] = []
        final_state: dict[str, Any] = {}
        last_signature = ""
        last_llm_trace_count = 0
        last_orchestration_trace_count = 0

        for turn_index in range(1, args.max_turns + 1):
            prompt = io_only_initial_prompt(manifest["id"]) if turn_index == 1 else io_only_continue_prompt(manifest["id"])
            messages.append({"role": "user", "content": prompt})
            stream_trace: list[dict[str, Any]] = []
            stream_started = time.time()
            for snapshot in agent.stream(prompt):
                stream_trace.append(summarize_state_snapshot(snapshot))
            final_state = dict(agent.state)
            serializable_state = serializable_agent_state(final_state, messages)
            api.exp_mgr.save_session_state(
                experiment["id"],
                session["id"],
                messages=messages,
                agent_state=serializable_state,
            )
            signature = state_signature(final_state)
            workflow_status = str(final_state.get("workflow_status") or "")
            llm_trace = list(final_state.get("llm_trace") or [])
            orchestration_trace = list(final_state.get("orchestration_trace") or [])
            turn_llm_entries = llm_trace[last_llm_trace_count:]
            turn_orchestration_entries = orchestration_trace[last_orchestration_trace_count:]
            turns.append(
                {
                    "turn_index": turn_index,
                    "prompt": prompt,
                    "started_at": datetime.fromtimestamp(stream_started, tz=timezone.utc).isoformat(),
                    "ended_at": now_iso(),
                    "duration_seconds": round(time.time() - stream_started, 3),
                    "workflow_status": workflow_status,
                    "current_step_id": final_state.get("current_step_id"),
                    "signature": signature,
                    "llm_call_count_delta": len(turn_llm_entries),
                    "orchestration_event_count_delta": len(turn_orchestration_entries),
                    "llm_usage_delta": aggregate_llm_usage(turn_llm_entries),
                    "llm_trace_delta_tail": trace_tail(turn_llm_entries),
                    "orchestration_trace_delta_tail": trace_tail(turn_orchestration_entries),
                    "trace": stream_trace,
                }
            )
            last_llm_trace_count = len(llm_trace)
            last_orchestration_trace_count = len(orchestration_trace)
            if workflow_status in {"success", "failed", "error"}:
                break
            if signature == last_signature:
                break
            last_signature = signature

        serializable_state = serializable_agent_state(final_state, messages)
        api.exp_mgr.save_session_state(
            experiment["id"],
            session["id"],
            messages=messages,
            agent_state=serializable_state,
        )

        session_state = client.get(
            f"/api/experiments/{experiment['id']}/sessions/{session['id']}"
        ).json()
        memory_items = fetch_memory_items(client, experiment["id"], session["id"])
        observed_outputs = collect_observed_outputs(workflow_dir)
        declared_outputs = evaluate_declared_outputs(workflow_dir, manifest)
        llm_usage_summary = aggregate_llm_usage(final_state.get("llm_trace"))
        step_metrics = build_agent_step_metrics(manifest, final_state, turns)
        workflow_status = (
            (session_state.get("agent_state") or {}).get("workflow_status")
            or (final_state.get("workflow_status"))
            or "failed"
        )
        payload = {
            "mode": "agent_io_only_skill_guided",
            "agent_name": agent_name,
            "llm_model": os.environ.get("LLM_MODEL") or os.environ.get("OPENROUTER_MODEL") or "",
            "workflow_step_selector_agent": os.environ.get("WORKFLOW_STEP_SELECTOR_AGENT") or "",
            "workflow_step_selector_model": os.environ.get("WORKFLOW_STEP_SELECTOR_MODEL") or "",
            "workflow_id": manifest.get("id"),
            "workflow_dir": str(workflow_dir),
            "finish_root": str(finish_root),
            "data_root": str(data_root),
            "skills_dir": str(skills_dir),
            "started_at": turns[0]["started_at"] if turns else now_iso(),
            "ended_at": now_iso(),
            "status": "success" if workflow_status == "success" else "failed",
            "workflow_status": workflow_status,
            "orchestration_mode": "skills_only",
            "manifest_step_graph_allowed": False,
            "loaded_skill_specs": loaded_skill_specs,
            "loaded_skill_count": len(loaded_skill_specs),
            "turn_count": len(turns),
            "turns": turns,
            "experiment": experiment,
            "session": session,
            "final_state": serializable_state,
            "final_session": session_state,
            "memory_items": memory_items,
            "llm_usage_summary": llm_usage_summary,
            "step_metrics": step_metrics,
            "declared_outputs": declared_outputs,
            "observed_outputs": observed_outputs,
            "llm_trace_tail": trace_tail(final_state.get("llm_trace")),
            "orchestration_trace_tail": trace_tail(final_state.get("orchestration_trace")),
        }
        payload = annotate_payload(payload, manifest=manifest, workflow_dir=workflow_dir)
        write_json(result_json, payload)
        return 0 if workflow_status == "success" else 1
    except Exception as error:
        write_json(
            result_json,
            worker_failure_payload(
                error,
                context={
                    "mode": "agent_io_only_skill_guided",
                    "agent_name": agent_name,
                    "workflow_dir": str(workflow_dir),
                    "finish_root": str(finish_root),
                    "data_root": str(data_root),
                    "result_json": str(result_json),
                },
            ),
        )
        return 1


def run_subprocess(
    command: list[str],
    *,
    timeout: int | None = None,
    extra_env: dict[str, str] | None = None,
) -> dict[str, Any]:
    started = time.time()
    env = build_runtime_env(extra_env)
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "started_at": datetime.fromtimestamp(started, tz=timezone.utc).isoformat(),
            "ended_at": now_iso(),
            "duration_seconds": round(time.time() - started, 3),
            "stdout": truncate_text(completed.stdout, limit=60_000),
            "stderr": truncate_text(completed.stderr, limit=60_000),
        }
    except subprocess.TimeoutExpired as error:
        return {
            "command": command,
            "returncode": -1,
            "started_at": datetime.fromtimestamp(started, tz=timezone.utc).isoformat(),
            "ended_at": now_iso(),
            "duration_seconds": round(time.time() - started, 3),
            "stdout": truncate_text(error.stdout, limit=60_000),
            "stderr": truncate_text(error.stderr, limit=60_000),
            "timed_out": True,
            "timeout_seconds": timeout,
        }


def start_subprocess(
    command: list[str],
    *,
    extra_env: dict[str, str] | None = None,
) -> tuple[subprocess.Popen[str], float, dict[str, Any]]:
    env = build_runtime_env(extra_env)
    started = time.time()
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    metadata = {
        "command": command,
        "started_at": datetime.fromtimestamp(started, tz=timezone.utc).isoformat(),
    }
    return proc, started, metadata


def wait_subprocess(
    proc: subprocess.Popen[str],
    started: float,
    metadata: dict[str, Any],
    *,
    timeout: int | None = None,
) -> dict[str, Any]:
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
        return {
            **metadata,
            "returncode": proc.returncode,
            "ended_at": now_iso(),
            "duration_seconds": round(time.time() - started, 3),
            "stdout": truncate_text(stdout, limit=60_000),
            "stderr": truncate_text(stderr, limit=60_000),
        }
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        return {
            **metadata,
            "returncode": -1,
            "ended_at": now_iso(),
            "duration_seconds": round(time.time() - started, 3),
            "stdout": truncate_text(stdout, limit=60_000),
            "stderr": truncate_text(stderr, limit=60_000),
            "timed_out": True,
            "timeout_seconds": timeout,
        }


def compare_output_sets(direct_payload: dict[str, Any], agent_payload: dict[str, Any]) -> dict[str, Any]:
    direct_index = {
        item["path"]: item
        for item in direct_payload.get("observed_outputs", [])
        if isinstance(item, dict) and item.get("path")
    }
    agent_index = {
        item["path"]: item
        for item in agent_payload.get("observed_outputs", [])
        if isinstance(item, dict) and item.get("path")
    }
    direct_outputs = set(direct_index)
    agent_outputs = set(agent_index)
    shared = sorted(direct_outputs & agent_outputs)
    direct_only = sorted(direct_outputs - agent_outputs)
    agent_only = sorted(agent_outputs - direct_outputs)
    hash_matches: list[str] = []
    hash_mismatches: list[str] = []
    hash_not_compared: list[str] = []
    for path in shared:
        direct_sha = direct_index[path].get("sha256")
        agent_sha = agent_index[path].get("sha256")
        if direct_sha and agent_sha:
            if direct_sha == agent_sha:
                hash_matches.append(path)
            else:
                hash_mismatches.append(path)
        else:
            hash_not_compared.append(path)
    return {
        "shared_output_count": len(shared),
        "direct_only_count": len(direct_only),
        "agent_only_count": len(agent_only),
        "shared_hash_match_count": len(hash_matches),
        "shared_hash_mismatch_count": len(hash_mismatches),
        "shared_hash_not_compared_count": len(hash_not_compared),
        "shared_outputs": shared,
        "direct_only_outputs": direct_only,
        "agent_only_outputs": agent_only,
        "shared_hash_matches": hash_matches,
        "shared_hash_mismatches": hash_mismatches,
        "shared_hash_not_compared": hash_not_compared,
    }


def summarize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    declared = payload.get("declared_outputs") or {}
    llm_usage = payload.get("llm_usage_summary") or aggregate_llm_usage(
        ((payload.get("final_state") or {}).get("llm_trace")) or payload.get("llm_trace")
    )
    step_metrics = payload.get("step_metrics") or []
    step_count = payload.get("step_count")
    if step_count is None:
        step_count = len(step_metrics) or len(((payload.get("final_state") or {}).get("workflow_plan") or {}).get("steps") or [])
    completed_step_count = payload.get("completed_step_count")
    if completed_step_count is None and isinstance(step_metrics, list):
        completed_step_count = sum(
            1
            for item in step_metrics
            if isinstance(item, dict)
            and str(item.get("execution_status") or item.get("plan_status") or "").lower() in {"success", "completed"}
        )
    started_at = payload.get("started_at") or (payload.get("final_state") or {}).get("started_at")
    ended_at = payload.get("ended_at") or (payload.get("final_state") or {}).get("ended_at")
    duration_seconds = None
    try:
        if started_at and ended_at:
            s = str(started_at).replace("Z", "+00:00")
            e = str(ended_at).replace("Z", "+00:00")
            duration_seconds = round((datetime.fromisoformat(e) - datetime.fromisoformat(s)).total_seconds(), 3)
    except Exception:
        duration_seconds = None
    return {
        "status": payload.get("status"),
        "workflow_status": payload.get("workflow_status", payload.get("status")),
        "evaluable": payload.get("evaluable"),
        "recommended_bucket": ((payload.get("evaluability") or {}).get("recommended_bucket")),
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_seconds": duration_seconds,
        "orchestration_mode": payload.get("orchestration_mode"),
        "manifest_step_graph_allowed": payload.get("manifest_step_graph_allowed"),
        "loaded_skill_count": payload.get("loaded_skill_count"),
        "declared_output_present_count": declared.get("present_count"),
        "declared_output_missing_count": declared.get("missing_count"),
        "declared_output_coverage": declared.get("coverage"),
        "observed_output_count": len(payload.get("observed_outputs") or []),
        "step_count": step_count,
        "completed_step_count": completed_step_count,
        "recovery_attempt_count": payload.get("recovery_attempt_count"),
        "false_success_claim": payload.get("false_success_claim"),
        "trace_node_count": ((payload.get("trace_tree") or {}).get("node_count")),
        "trace_stage_count": ((payload.get("trace_tree") or {}).get("stage_count")),
        "error_chain_length": len(payload.get("error_chain") or []),
        "onset_stage": ((payload.get("failure_onset") or {}).get("onset_stage")),
        "onset_turn": ((payload.get("failure_onset") or {}).get("onset_turn")),
        "onset_step_id": ((payload.get("failure_onset") or {}).get("onset_step_id")),
        "onset_category": ((payload.get("failure_onset") or {}).get("onset_category")),
        "terminal_symptom": payload.get("terminal_symptom"),
        "summary_faithfulness": payload.get("summary_faithfulness") or {},
        "workflow_noise_flags": payload.get("workflow_noise_flags") or [],
        "turn_count": payload.get("turn_count"),
        "llm_call_count": llm_usage.get("llm_call_count"),
        "token_recorded_call_count": llm_usage.get("token_recorded_call_count"),
        "prompt_tokens": llm_usage.get("prompt_tokens"),
        "completion_tokens": llm_usage.get("completion_tokens"),
        "total_tokens": llm_usage.get("total_tokens"),
        "reasoning_tokens": llm_usage.get("reasoning_tokens"),
        "cost": llm_usage.get("cost"),
    }


def parse_agent_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_agent_model_overrides(value: str | None) -> dict[str, str]:
    """Parse 'name=model,name2=model2' into a dict."""
    if not value:
        return {}
    overrides: dict[str, str] = {}
    for raw in value.split(","):
        part = raw.strip()
        if not part:
            continue
        if "=" not in part:
            continue
        name, model = part.split("=", 1)
        name = name.strip()
        model = model.strip()
        if name and model:
            overrides[name] = model
    return overrides


def parse_agent_python_overrides(value: str | None) -> dict[str, str]:
    """Parse 'name=/path/python,name2=/path/python2' into a dict."""
    if not value:
        return {}
    overrides: dict[str, str] = {}
    for raw in value.split(","):
        part = raw.strip()
        if not part:
            continue
        if "=" not in part:
            continue
        name, py = part.split("=", 1)
        name = name.strip()
        py = py.strip()
        if name and py:
            overrides[name] = py
    return overrides


def workflow_step_selection_prompt(agent_name: str) -> str | None:
    name = (agent_name or "").strip().lower()
    if name in {"", "renzo"}:
        return None
    if name == "biomni":
        return (
            "You are Biomni-style orchestration. Select the next workflow step to execute. "
            "Pick the step that maximizes downstream progress (unblocks more future steps) "
            "and has clearer expected outputs. Output only the chosen step id."
        )
    if name == "dswizard":
        return (
            "You are DSWizard-style orchestration. Select the next workflow step to execute. "
            "Prefer the most straightforward and dependency-respecting step that reduces uncertainty. "
            "Avoid risky choices when multiple steps are ready. Output only the chosen step id."
        )
    if name == "stella":
        return (
            "You are STELLA-style orchestration. Select the next workflow step to execute. "
            "Prefer steps that improve observability and validation (QC, reports, checks) when ready; "
            "otherwise pick the safest step with clear outputs. Output only the chosen step id."
        )
    if name == "tooluniverse":
        return (
            "You are ToolUniverse-style orchestration. Select the next workflow step to execute. "
            "Prefer steps with explicit outputs and strong IO contracts and that can run with currently "
            "available refs. Output only the chosen step id."
        )
    return None


def parse_main_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW_ID)
    parser.add_argument("--output-dir")
    parser.add_argument("--renzo-python")
    parser.add_argument("--agents", default="renzo,biomni,stella,tooluniverse")
    parser.add_argument("--baseline-agent", default="renzo")
    parser.add_argument("--agent-model", default="deepseek/deepseek-r1")
    parser.add_argument(
        "--agent-models",
        default="",
        help="Optional overrides in 'name=model,name2=model2' form (applies to --agents).",
    )
    parser.add_argument(
        "--agent-pythons",
        default="",
        help="Optional overrides in 'name=/abs/path/python,name2=/abs/path/python2' form (applies to --agents).",
    )
    parser.add_argument("--strict-agent-manifest", action="store_true")
    parser.add_argument("--shuffle-agent-steps", action="store_true")
    parser.add_argument("--timeout-per-step", type=int, default=3600)
    parser.add_argument("--max-agent-turns", type=int, default=20)
    parser.add_argument("--agent-process-timeout", type=int, default=21600)
    parser.add_argument("--parallel-runs", action="store_true")
    parser.add_argument(
        "--include-direct",
        action="store_true",
        help="Also run the legacy direct Snakemake baseline (disabled by default).",
    )
    parser.add_argument(
        "--require-real-frameworks",
        action="store_true",
        help="Require biomni/stella to run their real framework code (fail if unavailable).",
    )
    parser.add_argument(
        "--direct-dry-run",
        action="store_true",
        help="When --include-direct is set, use --dry-run for direct.",
    )
    return parser.parse_args(argv)


def parse_worker_direct_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-dir", required=True)
    parser.add_argument("--result-json", required=True)
    parser.add_argument("--timeout-per-step", type=int, default=3600)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def parse_worker_agent_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finish-root", required=True)
    parser.add_argument("--workflow-dir", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--result-json", required=True)
    parser.add_argument("--agent-name", default="renzo")
    parser.add_argument("--max-turns", type=int, default=20)
    parser.add_argument("--strict-manifest", action="store_true")
    return parser.parse_args(argv)


def parse_worker_peer_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-name", required=True)
    parser.add_argument("--finish-root", required=True)
    parser.add_argument("--workflow-dir", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--result-json", required=True)
    parser.add_argument("--timeout-per-step", type=int, default=3600)
    parser.add_argument("--strict-manifest", action="store_true")
    return parser.parse_args(argv)


def run_main(args: argparse.Namespace) -> int:
    source_workflow_dir = resolve_source_workflow_dir(args.workflow).resolve()
    manifest = load_workflow_manifest(source_workflow_dir)
    workflow_id = str(manifest["id"])
    renzo_python = resolve_renzo_python(args.renzo_python)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = Path(args.output_dir).resolve() if args.output_dir else (ROOT / "data" / "finish_run_comparisons" / f"{timestamp}-{workflow_id}")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    ensure_dir(output_dir)

    summary_json = output_dir / "artifacts" / "comparison-summary.json"
    cache_scope_base = workflow_id

    agents = parse_agent_list(getattr(args, "agents", "") or "")
    if not agents:
        agents = ["renzo"]
    baseline_agent = (getattr(args, "baseline_agent", "") or "renzo").strip() or "renzo"
    if baseline_agent not in agents:
        agents = [baseline_agent, *agents]

    model_overrides = parse_agent_model_overrides(getattr(args, "agent_models", "") or "")
    python_overrides = parse_agent_python_overrides(getattr(args, "agent_pythons", "") or "")
    default_models = {
        "renzo": args.agent_model,
        "biomni": "deepseek/deepseek-v3.2-exp",
        "dswizard": "deepseek/deepseek-v3.2-exp",
        "stella": "deepseek/deepseek-v3.2-exp",
        "tooluniverse": "deepseek/deepseek-v3.2-exp",
    }

    run_specs: list[dict[str, Any]] = []
    for agent_name in agents:
        agent_name = agent_name.strip()
        if not agent_name:
            continue
        model = model_overrides.get(agent_name) or default_models.get(agent_name) or args.agent_model
        python_bin = python_overrides.get(agent_name) or renzo_python
        agent_finish_root = ensure_dir(output_dir / "workdirs" / f"agent_{agent_name}" / "finish_root")
        agent_workflow_dir = copy_workflow_tree(source_workflow_dir, agent_finish_root / source_workflow_dir.name)
        if args.shuffle_agent_steps:
            rewrite_manifest_step_order(agent_workflow_dir, "reverse")
        agent_data_root = ensure_dir(output_dir / "workdirs" / f"agent_{agent_name}" / "data")
        result_json = output_dir / "artifacts" / f"agent-{agent_name}-run.json"
        run_specs.append(
            {
                "agent_name": agent_name,
                "model": model,
                "python": python_bin,
                "finish_root": agent_finish_root,
                "workflow_dir": agent_workflow_dir,
                "data_root": agent_data_root,
                "result_json": result_json,
            }
        )

    direct_process: dict[str, Any] | None = None
    direct_payload: dict[str, Any] | None = None
    direct_json: Path | None = None
    if bool(getattr(args, "include_direct", False)):
        direct_workflow_dir = copy_workflow_tree(source_workflow_dir, output_dir / "workdirs" / "direct" / source_workflow_dir.name)
        direct_json = output_dir / "artifacts" / "direct-run.json"
        direct_runtime_env = {
            "WORKFLOW_RUNTIME_CACHE_SCOPE": f"{cache_scope_base}-direct",
        }
        direct_command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "_worker_direct",
            "--workflow-dir",
            str(direct_workflow_dir),
            "--result-json",
            str(direct_json),
            "--timeout-per-step",
            str(args.timeout_per_step),
            *(["--dry-run"] if args.direct_dry_run else []),
        ]
        direct_process = run_subprocess(direct_command, extra_env=direct_runtime_env)
        direct_payload = read_json(direct_json) if direct_json.exists() else {"status": "failed", "error": "direct result JSON was not written"}

    processes: dict[str, Any] = {}
    payloads: dict[str, dict[str, Any]] = {}

    if args.parallel_runs:
        started_specs: list[tuple[str, subprocess.Popen[str], float, dict[str, Any]]] = []
        for spec in run_specs:
            agent_name = spec["agent_name"]
            result_json = spec["result_json"]
            agent_runtime_env = {
                "WORKFLOW_RUNTIME_CACHE_SCOPE": f"{cache_scope_base}-agent-{agent_name}",
                "LLM_MODEL": spec["model"],
                "OPENROUTER_MODEL": spec["model"],
            }
            if agent_name != "renzo":
                agent_runtime_env["WORKFLOW_STEP_SELECTOR_AGENT"] = agent_name
                agent_runtime_env["WORKFLOW_STEP_SELECTOR_MODEL"] = spec["model"]
                if agent_name == "biomni":
                    repo_dir = os.environ.get("BIOMNI_REPO_DIR", "/lab_workspace/projects/Biomni-main").strip()
                    shim_dir = str((ROOT / "peer_shims").resolve())
                    if repo_dir:
                        agent_runtime_env["PYTHONPATH"] = f"{shim_dir}:{repo_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
                    else:
                        agent_runtime_env["PYTHONPATH"] = f"{shim_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
                if agent_name == "stella":
                    stella_dir = os.environ.get("STELLA_DIR", "/lab_workspace/projects/RBioBench/agents_run/stella/STELLA").strip()
                    if stella_dir:
                        agent_runtime_env["STELLA_DIR"] = stella_dir
                        agent_runtime_env["PYTHONPATH"] = f"{stella_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
                if agent_name == "tooluniverse":
                    agent_runtime_env["TOOLUNIVERSE_HOME"] = str((Path(spec["data_root"]) / ".tooluniverse").resolve())
                    agent_runtime_env["TOOLUNIVERSE_LLM_CONFIG_MODE"] = "env_override"
                    agent_runtime_env["TOOLUNIVERSE_LLM_DEFAULT_PROVIDER"] = "OPENROUTER"
                    agent_runtime_env["TOOLUNIVERSE_LLM_MODEL_DEFAULT"] = spec["model"]
                if getattr(args, "require_real_frameworks", False) and agent_name in {"biomni", "stella", "tooluniverse"}:
                    agent_runtime_env["REQUIRE_REAL_AGENT_FRAMEWORK"] = "1"
            system_prompt = workflow_step_selection_prompt(agent_name)
            if system_prompt:
                agent_runtime_env["WORKFLOW_STEP_SELECTION_SYSTEM_PROMPT"] = system_prompt
            worker_name = "_worker_agent" if agent_name == "renzo" else "_worker_peer"
            agent_command = [
                str(spec["python"]),
                str(Path(__file__).resolve()),
                worker_name,
                "--finish-root",
                str(spec["finish_root"]),
                "--workflow-dir",
                str(spec["workflow_dir"]),
                "--data-root",
                str(spec["data_root"]),
                "--result-json",
                str(result_json),
                *(["--agent-name", str(agent_name)] if worker_name == "_worker_agent" else ["--agent-name", str(agent_name)]),
                *(["--max-turns", str(args.max_agent_turns)] if worker_name == "_worker_agent" else ["--timeout-per-step", str(args.timeout_per_step)]),
                *(["--strict-manifest"] if args.strict_agent_manifest else []),
            ]
            proc, started, meta = start_subprocess(agent_command, extra_env=agent_runtime_env)
            started_specs.append((agent_name, proc, started, meta))
        for agent_name, proc, started, meta in started_specs:
            processes[agent_name] = wait_subprocess(proc, started, meta, timeout=args.agent_process_timeout)
    else:
        for spec in run_specs:
            agent_name = spec["agent_name"]
            result_json = spec["result_json"]
            agent_runtime_env = {
                "WORKFLOW_RUNTIME_CACHE_SCOPE": f"{cache_scope_base}-agent-{agent_name}",
                "LLM_MODEL": spec["model"],
                "OPENROUTER_MODEL": spec["model"],
            }
            if agent_name != "renzo":
                agent_runtime_env["WORKFLOW_STEP_SELECTOR_AGENT"] = agent_name
                agent_runtime_env["WORKFLOW_STEP_SELECTOR_MODEL"] = spec["model"]
                if agent_name == "biomni":
                    repo_dir = os.environ.get("BIOMNI_REPO_DIR", "/lab_workspace/projects/Biomni-main").strip()
                    shim_dir = str((ROOT / "peer_shims").resolve())
                    if repo_dir:
                        agent_runtime_env["PYTHONPATH"] = f"{shim_dir}:{repo_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
                    else:
                        agent_runtime_env["PYTHONPATH"] = f"{shim_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
                if agent_name == "stella":
                    stella_dir = os.environ.get("STELLA_DIR", "/lab_workspace/projects/RBioBench/agents_run/stella/STELLA").strip()
                    if stella_dir:
                        agent_runtime_env["STELLA_DIR"] = stella_dir
                        agent_runtime_env["PYTHONPATH"] = f"{stella_dir}:{os.environ.get('PYTHONPATH', '')}".strip(":")
                if agent_name == "tooluniverse":
                    agent_runtime_env["TOOLUNIVERSE_HOME"] = str((Path(spec["data_root"]) / ".tooluniverse").resolve())
                    agent_runtime_env["TOOLUNIVERSE_LLM_CONFIG_MODE"] = "env_override"
                    agent_runtime_env["TOOLUNIVERSE_LLM_DEFAULT_PROVIDER"] = "OPENROUTER"
                    agent_runtime_env["TOOLUNIVERSE_LLM_MODEL_DEFAULT"] = spec["model"]
                if getattr(args, "require_real_frameworks", False) and agent_name in {"biomni", "stella", "tooluniverse"}:
                    agent_runtime_env["REQUIRE_REAL_AGENT_FRAMEWORK"] = "1"
            system_prompt = workflow_step_selection_prompt(agent_name)
            if system_prompt:
                agent_runtime_env["WORKFLOW_STEP_SELECTION_SYSTEM_PROMPT"] = system_prompt
            worker_name = "_worker_agent" if agent_name == "renzo" else "_worker_peer"
            agent_command = [
                str(spec["python"]),
                str(Path(__file__).resolve()),
                worker_name,
                "--finish-root",
                str(spec["finish_root"]),
                "--workflow-dir",
                str(spec["workflow_dir"]),
                "--data-root",
                str(spec["data_root"]),
                "--result-json",
                str(result_json),
                *(["--agent-name", str(agent_name)] if worker_name == "_worker_agent" else ["--agent-name", str(agent_name)]),
                *(["--max-turns", str(args.max_agent_turns)] if worker_name == "_worker_agent" else ["--timeout-per-step", str(args.timeout_per_step)]),
                *(["--strict-manifest"] if args.strict_agent_manifest else []),
            ]
            processes[agent_name] = run_subprocess(
                agent_command,
                timeout=args.agent_process_timeout,
                extra_env=agent_runtime_env,
            )

    for spec in run_specs:
        agent_name = spec["agent_name"]
        result_json = Path(spec["result_json"])
        payloads[agent_name] = read_json(result_json) if result_json.exists() else {"status": "failed", "error": "agent result JSON was not written"}

    output_comparisons: dict[str, Any] = {}
    baseline_payload = payloads.get(baseline_agent) or {}
    for agent_name, agent_payload in payloads.items():
        if agent_name == baseline_agent:
            continue
        output_comparisons[agent_name] = compare_output_sets(baseline_payload, agent_payload)

    artifacts: dict[str, Any] = {
        "comparison_summary_json": str(summary_json),
        "agents": {name: str((output_dir / "artifacts" / f"agent-{name}-run.json")) for name in payloads.keys()},
    }
    if direct_json is not None:
        artifacts["direct_run_json"] = str(direct_json)

    summary = {
        "created_at": now_iso(),
        "workflow_id": workflow_id,
        "source_workflow_dir": str(source_workflow_dir),
        "output_dir": str(output_dir),
        "renzo_python": renzo_python,
        "baseline_agent": baseline_agent,
        "agents": agents,
        "agent_models": {spec["agent_name"]: spec["model"] for spec in run_specs},
        "agent_strict_manifest": bool(args.strict_agent_manifest),
        "agent_manifest_rewritten": "reverse" if args.shuffle_agent_steps else "original",
        "include_direct": bool(getattr(args, "include_direct", False)),
        "artifacts": artifacts,
        "processes": {
            **({"direct": direct_process} if direct_process is not None else {}),
            "agents": processes,
        },
        "runs": {
            **({"direct": summarize_payload(direct_payload or {})} if direct_payload is not None else {}),
            "agents": {name: summarize_payload(payload) for name, payload in payloads.items()},
        },
        "output_comparisons_vs_baseline": output_comparisons,
    }
    write_json(summary_json, summary)
    print(summary_json)
    print(
        json.dumps(
            {
                "workflow_id": workflow_id,
                "baseline_agent": baseline_agent,
                "agent_statuses": {
                    name: summary["runs"]["agents"][name]["status"]
                    for name in summary["runs"]["agents"]
                },
                "output_dir": str(output_dir),
            },
            ensure_ascii=False,
        )
    )
    agent_ok = all(proc.get("returncode", 1) == 0 for proc in processes.values())
    direct_ok = True
    if direct_process is not None:
        direct_ok = direct_process.get("returncode", 1) == 0
    return 0 if agent_ok and direct_ok else 1


def run_worker_peer(args: argparse.Namespace) -> int:
    peer_args = argparse.Namespace(
        finish_root=args.finish_root,
        workflow_dir=args.workflow_dir,
        data_root=args.data_root,
        result_json=args.result_json,
        agent_name=args.agent_name,
        max_turns=20,
        strict_manifest=bool(args.strict_manifest),
    )
    return run_worker_agent(peer_args)


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "_worker_direct":
        return run_worker_direct(parse_worker_direct_args(args[1:]))
    if args and args[0] == "_worker_agent":
        return run_worker_agent(parse_worker_agent_args(args[1:]))
    if args and args[0] == "_worker_peer":
        return run_worker_peer(parse_worker_peer_args(args[1:]))
    return run_main(parse_main_args(args))


if __name__ == "__main__":
    raise SystemExit(main())
