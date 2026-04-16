"""Experiment workspace management with session-based isolation.

Directory layout:

    renzo/data/experiments/{experiment_id}/
        metadata.json        # name, description, dataset_ids, status
        sessions/
            {session_id}/
                session.json # messages, agent_state snapshot, timestamps
                output/      # artifacts produced in this session

Experiments reference datasets (independent entities) and contain sessions.
Each session is a conversation with the agent that produces artifacts.
"""
from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid
import logging

from renzo.app.tracing import compact_trace_entries

logger = logging.getLogger(__name__)

_default_data_root = (Path(__file__).resolve().parent.parent / "data").resolve()
_data_root = Path(os.environ.get("DATA_ROOT", str(_default_data_root))).resolve()
EXPERIMENTS_ROOT = _data_root / "experiments"
EXPERIMENTS_ROOT.mkdir(parents=True, exist_ok=True)

MAX_PERSISTED_MESSAGES = 200
MAX_PERSISTED_LOGS = 50
MAX_TEXT_FIELD_LEN = 20000
MAX_ARTIFACT_PREVIEW_LEN = 4000
MAX_INLINE_MESSAGES = 60
MAX_INLINE_LOGS = 10
MAX_INLINE_TEXT_LEN = 4000
MEMORY_DIRNAME = "memory"

OFFLOAD_JSON_KEYS = {
    "data_profile",
    "execution_logs",
    "artifact_index",
    "workflow_plan",
    "workflow_run_context",
    "qc_results",
    "plan_steps",
    "llm_trace",
    "orchestration_trace",
}

OFFLOAD_TEXT_KEYS = {
    "long_term_summary": "summary.md",
    "goal": "goal.md",
    "dataset_context": "dataset_context.md",
    "code_scratchpad": "code_scratchpad.txt",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ══════════════════════════════════════════════════════════════════════
# Experiment CRUD
# ══════════════════════════════════════════════════════════════════════

def create_experiment(
    name: str,
    description: str = "",
    dataset_ids: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    workflow_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new experiment workspace on disk."""
    exp_id = f"exp-{uuid.uuid4().hex[:12]}"
    exp_dir = EXPERIMENTS_ROOT / exp_id
    (exp_dir / "sessions").mkdir(parents=True, exist_ok=True)

    metadata: Dict[str, Any] = {
        "id": exp_id,
        "name": name,
        "description": description,
        "dataset_ids": dataset_ids or [],
        "tags": tags or [],
        "status": "active",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "session_count": 0,
        "total_size_bytes": 0,
    }
    if workflow_id:
        metadata["workflow_id"] = workflow_id
    _save_metadata(exp_id, metadata)
    logger.info("Created experiment %s at %s", exp_id, exp_dir)
    return metadata


def duplicate_experiment(exp_id: str, new_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Create a copy of an experiment (metadata only, no sessions copied)."""
    src = get_experiment(exp_id)
    if src is None:
        return None
    return create_experiment(
        name=new_name or f"{src['name']} (copy)",
        description=src.get("description", ""),
        dataset_ids=src.get("dataset_ids", []),
        tags=src.get("tags", []),
        workflow_id=src.get("workflow_id"),
    )


def get_experiment(exp_id: str) -> Optional[Dict[str, Any]]:
    """Load experiment metadata from disk."""
    meta_path = EXPERIMENTS_ROOT / exp_id / "metadata.json"
    if not meta_path.exists():
        return None
    with open(meta_path, "r") as f:
        return json.load(f)


def list_experiments(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all experiments, optionally filtered by status."""
    results = []
    if not EXPERIMENTS_ROOT.exists():
        return results
    for entry in sorted(EXPERIMENTS_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        meta_path = entry / "metadata.json"
        if not meta_path.exists():
            continue
        with open(meta_path, "r") as f:
            meta = json.load(f)
        if status and meta.get("status") != status:
            continue
        _refresh_experiment_counts(meta)
        results.append(meta)
    results.sort(key=lambda m: m.get("created_at", ""), reverse=True)
    return results


def update_experiment(
    exp_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[List[str]] = None,
    dataset_ids: Optional[List[str]] = None,
    workflow_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Update experiment metadata fields."""
    meta = get_experiment(exp_id)
    if meta is None:
        return None
    if name is not None:
        meta["name"] = name
    if description is not None:
        meta["description"] = description
    if status is not None:
        meta["status"] = status
    if tags is not None:
        meta["tags"] = tags
    if dataset_ids is not None:
        meta["dataset_ids"] = dataset_ids
    if workflow_id is not None:
        meta["workflow_id"] = workflow_id
    meta["updated_at"] = _now_iso()
    _save_metadata(exp_id, meta)
    return meta


def delete_experiment(exp_id: str) -> bool:
    """Delete an experiment and all its data."""
    exp_dir = EXPERIMENTS_ROOT / exp_id
    if not exp_dir.exists():
        return False
    shutil.rmtree(exp_dir)
    logger.info("Deleted experiment %s", exp_id)
    return True


# ══════════════════════════════════════════════════════════════════════
# Session management (within an experiment)
# ══════════════════════════════════════════════════════════════════════

def create_session(
    exp_id: str,
    name: str = "",
) -> Optional[Dict[str, Any]]:
    """Create a new session within an experiment."""
    exp_dir = EXPERIMENTS_ROOT / exp_id
    if not exp_dir.exists():
        return None

    sess_id = f"sess-{uuid.uuid4().hex[:12]}"
    sess_dir = exp_dir / "sessions" / sess_id
    (sess_dir / "output").mkdir(parents=True, exist_ok=True)

    session_data: Dict[str, Any] = {
        "id": sess_id,
        "experiment_id": exp_id,
        "name": name or f"Session {sess_id[:16]}",
        "messages": [],
        "agent_state": {},
        "status": "active",
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }
    _save_session(exp_id, sess_id, session_data)
    logger.info("Created session %s in experiment %s", sess_id, exp_id)
    return session_data


def get_session(exp_id: str, sess_id: str) -> Optional[Dict[str, Any]]:
    """Load session data from disk."""
    sess_path = EXPERIMENTS_ROOT / exp_id / "sessions" / sess_id / "session.json"
    if not sess_path.exists():
        return None
    with open(sess_path, "r") as f:
        return json.load(f)


def get_session_hydrated(exp_id: str, sess_id: str) -> Optional[Dict[str, Any]]:
    """Load session and hydrate offloaded state/message fields from memory items."""
    session = get_session(exp_id, sess_id)
    if not session:
        return None

    hydrated = dict(session)
    manifest = get_session_memory_manifest(exp_id, sess_id)
    items = manifest.get("items", {}) if isinstance(manifest, dict) else {}

    # Hydrate full messages when available.
    msg_item = items.get("messages_full")
    if isinstance(msg_item, dict):
        item = read_session_memory_item(exp_id, sess_id, "messages_full")
        if item and isinstance(item.get("content"), list):
            hydrated["messages"] = item["content"]

    # Strip code blocks from assistant messages so restored sessions display cleanly.
    hydrated["messages"] = _sanitize_messages(hydrated.get("messages") or [])

    # Hydrate offloaded JSON state keys.
    agent_state = dict(hydrated.get("agent_state") or {})
    for key in OFFLOAD_JSON_KEYS:
        item_key = f"state.{key}"
        if not isinstance(items.get(item_key), dict):
            continue
        item = read_session_memory_item(exp_id, sess_id, item_key)
        if item and "content" in item:
            agent_state[key] = item["content"]

    # Hydrate offloaded text state keys.
    for key in OFFLOAD_TEXT_KEYS:
        if not isinstance(items.get(key), dict):
            continue
        item = read_session_memory_item(exp_id, sess_id, key)
        if item and isinstance(item.get("content"), str):
            agent_state[key] = item["content"]

    hydrated["agent_state"] = agent_state
    # Restore QC table on last assistant message from agent_state.qc_results (for sessions saved before we persisted qc_table)
    messages = hydrated.get("messages") or []
    qc_results = agent_state.get("qc_results") or []
    if messages and qc_results:
        last_qc = qc_results[-1] if isinstance(qc_results[-1], dict) else {}
        details = last_qc.get("details") if isinstance(last_qc.get("details"), list) else None
        if details:
            for i in range(len(messages) - 1, -1, -1):
                m = messages[i]
                if isinstance(m, dict) and (m.get("role") or m.get("type")) == "assistant":
                    if not m.get("qc_table"):
                        m["qc_table"] = details
                    break
    hydrated["memory_manifest"] = manifest
    return hydrated


def list_sessions(exp_id: str) -> List[Dict[str, Any]]:
    """List all sessions in an experiment."""
    sessions_dir = EXPERIMENTS_ROOT / exp_id / "sessions"
    if not sessions_dir.exists():
        return []
    results = []
    for entry in sorted(sessions_dir.iterdir()):
        if not entry.is_dir():
            continue
        sess_path = entry / "session.json"
        if not sess_path.exists():
            continue
        with open(sess_path, "r") as f:
            data = json.load(f)
        # Return summary (exclude full messages/state for list view)
        results.append({
            "id": data.get("id", entry.name),
            "experiment_id": exp_id,
            "name": data.get("name", ""),
            "status": data.get("status", "active"),
            "message_count": len(data.get("messages", [])),
            "created_at": data.get("created_at", ""),
            "updated_at": data.get("updated_at", ""),
        })
    results.sort(key=lambda s: s.get("created_at", ""), reverse=True)
    return results


def save_session_state(
    exp_id: str,
    sess_id: str,
    messages: Optional[List[Dict]] = None,
    agent_state: Optional[Dict] = None,
) -> bool:
    """Persist session state (messages + agent state snapshot) to disk.

    Called after each agent step to ensure durability.
    """
    session = get_session(exp_id, sess_id)
    if session is None:
        return False
    memory_manifest = get_session_memory_manifest(exp_id, sess_id) or {"updated_at": _now_iso(), "items": {}}
    if messages is not None:
        safe_messages = _sanitize_messages(messages)
        memory_manifest = _persist_messages_memory(exp_id, sess_id, safe_messages, memory_manifest)
        session["messages"] = _compact_messages_inline(safe_messages)
    if agent_state is not None:
        # Persist full state to memory files and keep compact inline state.
        safe_state = _sanitize_agent_state(agent_state, compact=False)
        memory_manifest = _persist_state_memory(exp_id, sess_id, safe_state, memory_manifest)
        session["agent_state"] = _compact_agent_state_inline(safe_state)
    memory_manifest["updated_at"] = _now_iso()
    _save_memory_manifest(exp_id, sess_id, memory_manifest)
    session["memory_manifest"] = memory_manifest
    session["updated_at"] = _now_iso()
    _save_session(exp_id, sess_id, session)
    return True


def delete_session(exp_id: str, sess_id: str) -> bool:
    """Delete a session and all its output."""
    sess_dir = EXPERIMENTS_ROOT / exp_id / "sessions" / sess_id
    if not sess_dir.exists():
        return False
    shutil.rmtree(sess_dir)
    logger.info("Deleted session %s from experiment %s", sess_id, exp_id)
    return True


def cleanup_old_sessions(
    exp_id: str,
    *,
    max_age_days: Optional[int] = None,
    max_sessions: Optional[int] = None,
) -> int:
    """Delete sessions in an experiment that are older than max_age_days or beyond max_sessions (keep newest).
    Returns number of sessions deleted."""
    deleted = 0
    sessions_list = list_sessions(exp_id)
    if not sessions_list:
        return 0
    now = datetime.now(timezone.utc)
    to_delete: List[str] = []
    if max_age_days is not None and max_age_days > 0:
        for s in sessions_list:
            updated = s.get("updated_at") or s.get("created_at") or ""
            if not updated:
                continue
            try:
                dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                if (now - dt).total_seconds() > max_age_days * 86400:
                    to_delete.append(s["id"])
            except (ValueError, TypeError):
                pass
    if max_sessions is not None and max_sessions >= 0:
        # Keep newest max_sessions; mark rest for deletion (if not already in to_delete)
        by_created = sorted(sessions_list, key=lambda x: x.get("created_at", ""), reverse=True)
        for s in by_created[max_sessions:]:
            if s["id"] not in to_delete:
                to_delete.append(s["id"])
    for sess_id in to_delete:
        if delete_session(exp_id, sess_id):
            deleted += 1
    if deleted:
        meta = get_experiment(exp_id)
        if meta:
            _refresh_experiment_counts(meta)
            _save_metadata(exp_id, meta)
    return deleted


def cleanup_all_old_sessions(
    max_age_days: Optional[int] = None,
    max_sessions_per_experiment: Optional[int] = None,
) -> Dict[str, int]:
    """Run cleanup_old_sessions for every experiment. Returns { 'experiments': N, 'sessions_deleted': M }."""
    total_deleted = 0
    exp_ids = [e.name for e in EXPERIMENTS_ROOT.iterdir() if (EXPERIMENTS_ROOT / e.name / "metadata.json").exists()]
    for exp_id in exp_ids:
        n = cleanup_old_sessions(
            exp_id,
            max_age_days=max_age_days,
            max_sessions=max_sessions_per_experiment,
        )
        total_deleted += n
    return {"experiments_processed": len(exp_ids), "sessions_deleted": total_deleted}


def get_session_output_dir(exp_id: str, sess_id: str) -> Optional[Path]:
    """Get the output directory for a session. Creates it if needed."""
    output_dir = EXPERIMENTS_ROOT / exp_id / "sessions" / sess_id / "output"
    if not output_dir.parent.exists():
        return None
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_session_memory_manifest(exp_id: str, sess_id: str) -> Dict[str, Any]:
    manifest_path = _session_memory_dir(exp_id, sess_id) / "index.json"
    if manifest_path.exists():
        with open(manifest_path, "r") as f:
            return json.load(f)
    session = get_session(exp_id, sess_id)
    if session and isinstance(session.get("memory_manifest"), dict):
        return session["memory_manifest"]
    return {"updated_at": "", "items": {}}


def read_session_memory_item(exp_id: str, sess_id: str, item_id: str) -> Optional[Dict[str, Any]]:
    manifest = get_session_memory_manifest(exp_id, sess_id)
    items = manifest.get("items", {})
    item = items.get(item_id)
    if not isinstance(item, dict):
        return None
    rel_path = item.get("path")
    if not rel_path:
        return None
    mem_dir = _session_memory_dir(exp_id, sess_id).resolve()
    abs_path = (mem_dir / rel_path).resolve()
    if not str(abs_path).startswith(str(mem_dir)):
        return None
    if not abs_path.exists() or not abs_path.is_file():
        return None

    item_type = item.get("type", "json")
    try:
        if item_type == "json":
            with open(abs_path, "r") as f:
                content = json.load(f)
        else:
            with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        return {
            "item_id": item_id,
            "type": item_type,
            "path": rel_path,
            "updated_at": item.get("updated_at", ""),
            "content": content,
        }
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════
# Backward-compatible helpers (used by executor/step_finalize)
# ══════════════════════════════════════════════════════════════════════

def get_experiment_dir(exp_id: str, subdir: str = "") -> Optional[Path]:
    """Get experiment directory or subdirectory path.

    For backward compat with old code that references 'output' etc.
    With the new model, callers should use get_session_output_dir instead.
    """
    exp_dir = EXPERIMENTS_ROOT / exp_id
    if not exp_dir.exists():
        return None
    if subdir:
        target = exp_dir / subdir
        target.mkdir(parents=True, exist_ok=True)
        return target
    return exp_dir


def resolve_execution_workdir(
    experiment_id: Optional[str],
    session_id: Optional[str],
    artifact_policy: str = "session",
) -> Path:
    """Resolve the canonical output directory for a run.

    Priority:
    1. session output dir (artifact_policy=session and IDs available)
    2. experiment output dir
    3. shared renzo/data/artifacts fallback
    """
    if artifact_policy == "session" and experiment_id and session_id:
        sess_dir = get_session_output_dir(experiment_id, session_id)
        if sess_dir:
            return sess_dir

    if experiment_id:
        exp_out = get_experiment_dir(experiment_id, "output")
        if exp_out:
            return exp_out

    return Path(__file__).parent.parent / "data" / "artifacts"


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

def _save_metadata(exp_id: str, meta: Dict[str, Any]) -> None:
    meta_path = EXPERIMENTS_ROOT / exp_id / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def _save_session(exp_id: str, sess_id: str, data: Dict[str, Any]) -> None:
    sess_path = EXPERIMENTS_ROOT / exp_id / "sessions" / sess_id / "session.json"
    sess_path.parent.mkdir(parents=True, exist_ok=True)
    with open(sess_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _refresh_experiment_counts(meta: Dict[str, Any]) -> None:
    """Recount sessions and total output size."""
    exp_dir = EXPERIMENTS_ROOT / meta["id"]
    sessions_dir = exp_dir / "sessions"
    total_size = 0
    session_count = 0
    if sessions_dir.exists():
        for entry in sessions_dir.iterdir():
            if entry.is_dir() and (entry / "session.json").exists():
                session_count += 1
                output_dir = entry / "output"
                if output_dir.exists():
                    for f in output_dir.rglob("*"):
                        if f.is_file():
                            total_size += f.stat().st_size
    meta["session_count"] = session_count
    meta["total_size_bytes"] = total_size
    meta["updated_at"] = _now_iso()


def _strip_markdown_code_blocks(text: str) -> str:
    """Remove markdown code blocks so restored assistant content does not show raw code."""
    return re.sub(r"```[\w{}\s]*\n.*?```", "(output omitted)", text, flags=re.DOTALL)


def _sanitize_messages(messages: List[Dict]) -> List[Dict[str, Any]]:
    safe_messages: List[Dict[str, Any]] = []
    for m in messages:
        msg = dict(m)
        content = msg.get("content")
        if isinstance(content, str):
            if msg.get("role") == "assistant":
                content = _strip_markdown_code_blocks(content)
            if len(content) > MAX_TEXT_FIELD_LEN:
                msg["content"] = content[-MAX_TEXT_FIELD_LEN:]
            else:
                msg["content"] = content
        safe_messages.append(msg)
    return safe_messages


def _compact_messages_inline(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return messages[-MAX_INLINE_MESSAGES:]


def _sanitize_agent_state(state: Dict, compact: bool = True) -> Dict:
    """Remove non-JSON-serializable items from agent state."""
    safe = {}
    skip_keys = {"messages", "know_how_documents"}  # handled separately or too large
    for k, v in state.items():
        if k in skip_keys:
            continue
        if k.startswith("_"):
            continue
        try:
            json.dumps(v)
            safe[k] = v
        except (TypeError, ValueError):
            safe[k] = str(v)

    if not compact:
        return safe

    # Bound heavy fields to keep session payloads stable.
    code = safe.get("code_scratchpad")
    if isinstance(code, str) and len(code) > MAX_TEXT_FIELD_LEN:
        safe["code_scratchpad"] = code[-MAX_TEXT_FIELD_LEN:]

    logs = safe.get("execution_logs")
    if isinstance(logs, list):
        slim_logs: List[Dict[str, Any]] = []
        for raw in logs[-MAX_PERSISTED_LOGS:]:
            if not isinstance(raw, dict):
                continue
            log = dict(raw)
            for key in ("stdout", "stderr"):
                value = log.get(key)
                if isinstance(value, str) and len(value) > MAX_TEXT_FIELD_LEN:
                    log[key] = value[-MAX_TEXT_FIELD_LEN:]
            slim_logs.append(log)
        safe["execution_logs"] = slim_logs

    artifacts = safe.get("artifact_index")
    if isinstance(artifacts, list):
        slim_artifacts: List[Dict[str, Any]] = []
        for raw in artifacts:
            if not isinstance(raw, dict):
                continue
            art = dict(raw)
            preview = art.get("preview")
            if isinstance(preview, str) and len(preview) > MAX_ARTIFACT_PREVIEW_LEN:
                art["preview"] = preview[:MAX_ARTIFACT_PREVIEW_LEN]
            slim_artifacts.append(art)
        safe["artifact_index"] = slim_artifacts

    safe["llm_trace"] = compact_trace_entries(
        safe.get("llm_trace"),
        max_events=MAX_PERSISTED_LOGS,
        max_text_len=MAX_TEXT_FIELD_LEN,
    )
    safe["orchestration_trace"] = compact_trace_entries(
        safe.get("orchestration_trace"),
        max_events=MAX_PERSISTED_LOGS,
        max_text_len=MAX_TEXT_FIELD_LEN,
    )
    return safe


def _compact_agent_state_inline(state: Dict[str, Any]) -> Dict[str, Any]:
    compacted = _sanitize_agent_state(state, compact=True)
    logs = compacted.get("execution_logs")
    if isinstance(logs, list):
        trimmed_logs: List[Dict[str, Any]] = []
        for raw in logs[-MAX_INLINE_LOGS:]:
            if not isinstance(raw, dict):
                continue
            log = dict(raw)
            for key in ("stdout", "stderr"):
                value = log.get(key)
                if isinstance(value, str) and len(value) > MAX_INLINE_TEXT_LEN:
                    log[key] = value[-MAX_INLINE_TEXT_LEN:]
            trimmed_logs.append(log)
        compacted["execution_logs"] = trimmed_logs

    code = compacted.get("code_scratchpad")
    if isinstance(code, str) and len(code) > MAX_INLINE_TEXT_LEN:
        compacted["code_scratchpad"] = code[-MAX_INLINE_TEXT_LEN:]
    compacted["llm_trace"] = compact_trace_entries(
        compacted.get("llm_trace"),
        max_events=MAX_INLINE_LOGS,
        max_text_len=MAX_INLINE_TEXT_LEN,
    )
    compacted["orchestration_trace"] = compact_trace_entries(
        compacted.get("orchestration_trace"),
        max_events=MAX_INLINE_LOGS,
        max_text_len=MAX_INLINE_TEXT_LEN,
    )
    return compacted


def _session_memory_dir(exp_id: str, sess_id: str) -> Path:
    return EXPERIMENTS_ROOT / exp_id / "sessions" / sess_id / MEMORY_DIRNAME


def _save_memory_manifest(exp_id: str, sess_id: str, manifest: Dict[str, Any]) -> None:
    mem_dir = _session_memory_dir(exp_id, sess_id)
    mem_dir.mkdir(parents=True, exist_ok=True)
    with open(mem_dir / "index.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def _persist_messages_memory(
    exp_id: str,
    sess_id: str,
    messages: List[Dict[str, Any]],
    manifest: Dict[str, Any],
) -> Dict[str, Any]:
    mem_dir = _session_memory_dir(exp_id, sess_id)
    mem_dir.mkdir(parents=True, exist_ok=True)
    rel_path = "messages.full.json"
    abs_path = mem_dir / rel_path
    with open(abs_path, "w") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    manifest.setdefault("items", {})["messages_full"] = {
        "type": "json",
        "path": rel_path,
        "size_bytes": abs_path.stat().st_size,
        "updated_at": _now_iso(),
    }
    return manifest


def _persist_state_memory(
    exp_id: str,
    sess_id: str,
    state: Dict[str, Any],
    manifest: Dict[str, Any],
) -> Dict[str, Any]:
    mem_dir = _session_memory_dir(exp_id, sess_id)
    mem_dir.mkdir(parents=True, exist_ok=True)
    items = manifest.setdefault("items", {})

    for key in OFFLOAD_JSON_KEYS:
        if key not in state:
            continue
        rel_path = f"state.{key}.json"
        abs_path = mem_dir / rel_path
        with open(abs_path, "w") as f:
            json.dump(state[key], f, indent=2, ensure_ascii=False)
        items[f"state.{key}"] = {
            "type": "json",
            "path": rel_path,
            "size_bytes": abs_path.stat().st_size,
            "updated_at": _now_iso(),
        }

    for key, rel_path in OFFLOAD_TEXT_KEYS.items():
        value = state.get(key)
        if not isinstance(value, str) or not value:
            continue
        abs_path = mem_dir / rel_path
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(value)
        items[key] = {
            "type": "text",
            "path": rel_path,
            "size_bytes": abs_path.stat().st_size,
            "updated_at": _now_iso(),
        }

    return manifest
