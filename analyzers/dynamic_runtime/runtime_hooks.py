from __future__ import annotations

import atexit
import asyncio
import hashlib
import json
import multiprocessing
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

EVENT_LOG_PATH = os.getenv("AGENTIC_EVENT_LOG", "/tmp/agentic_events.jsonl")
JOB_ID = os.getenv("AGENTIC_JOB_ID", "unknown_job")
RUN_ID = os.getenv("AGENTIC_RUN_ID", "run_0")

_lock = threading.Lock()
_async_peak = 0
_async_inflight = 0
_thread_peak = threading.active_count()
_process_peak = 1


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_parent() -> None:
    Path(EVENT_LOG_PATH).parent.mkdir(parents=True, exist_ok=True)


def _update_peaks() -> None:
    global _thread_peak, _process_peak
    _thread_peak = max(_thread_peak, threading.active_count())
    _process_peak = max(_process_peak, len(multiprocessing.active_children()) + 1)


def emit_event(event_type: str, phase: str, payload: dict[str, Any] | None = None) -> None:
    _ensure_parent()
    _update_peaks()
    record = {
        "timestamp": _utc_iso(),
        "job_id": JOB_ID,
        "run_id": RUN_ID,
        "phase": phase,
        "event_type": event_type,
        "actor": "instrumented_runtime",
        "target": None,
        "payload": payload or {},
        "trace_id": None,
    }
    line = json.dumps(record, ensure_ascii=False)
    with _lock:
        with open(EVENT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def _prompt_from_call(args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    for key in ("prompt", "input", "system_prompt"):
        if key in kwargs and isinstance(kwargs[key], str):
            return kwargs[key]
    messages = kwargs.get("messages")
    if isinstance(messages, list):
        chunks: list[str] = []
        for item in messages:
            if isinstance(item, dict):
                content = item.get("content")
                if isinstance(content, str):
                    chunks.append(content)
        return "\n".join(chunks)
    for arg in args:
        if isinstance(arg, str):
            return arg
    return ""


def _extract_usage(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage", None)
    if usage is None and isinstance(response, dict):
        usage = response.get("usage")
    if usage is None:
        return {}
    if hasattr(usage, "model_dump"):
        usage = usage.model_dump()
    if hasattr(usage, "__dict__"):
        usage = usage.__dict__
    if not isinstance(usage, dict):
        return {}
    out: dict[str, int] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens", "input_tokens", "output_tokens"):
        value = usage.get(key)
        if isinstance(value, int):
            out[key] = value
    return out


def ac_track_call(kind: str, target: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    global _async_inflight, _async_peak
    start = time.perf_counter()
    prompt_text = _prompt_from_call(args, kwargs)
    template_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()[:16] if prompt_text else None
    emit_event(
        event_type="call_start",
        phase=kind,
        payload={
            "kind": kind,
            "target": target,
            "prompt_chars": len(prompt_text),
            "template_hash": template_hash,
            "bytes_in": len(json.dumps({"args": str(args), "kwargs": str(kwargs)}, ensure_ascii=False)),
        },
    )
    try:
        result = func(*args, **kwargs)
        if asyncio.iscoroutine(result):
            _async_inflight += 1
            _async_peak = max(_async_peak, _async_inflight)

            async def _await_and_log() -> Any:
                global _async_inflight
                try:
                    value = await result
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    payload = {
                        "kind": kind,
                        "target": target,
                        "duration_ms": elapsed_ms,
                        "prompt_chars": len(prompt_text),
                        "template_hash": template_hash,
                        "usage": _extract_usage(value),
                        "bytes_out": len(str(value)) if value is not None else 0,
                    }
                    emit_event(event_type="call_end", phase=kind, payload=payload)
                    return value
                except Exception as exc:  # pragma: no cover
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    emit_event(
                        event_type="call_error",
                        phase=kind,
                        payload={
                            "kind": kind,
                            "target": target,
                            "duration_ms": elapsed_ms,
                            "error": type(exc).__name__,
                            "message": str(exc)[:400],
                        },
                    )
                    raise
                finally:
                    _async_inflight = max(0, _async_inflight - 1)

            return _await_and_log()
        elapsed_ms = (time.perf_counter() - start) * 1000
        payload = {
            "kind": kind,
            "target": target,
            "duration_ms": elapsed_ms,
            "prompt_chars": len(prompt_text),
            "template_hash": template_hash,
            "usage": _extract_usage(result),
            "bytes_out": len(str(result)) if result is not None else 0,
        }
        emit_event(event_type="call_end", phase=kind, payload=payload)
        return result
    except Exception as exc:  # pragma: no cover
        elapsed_ms = (time.perf_counter() - start) * 1000
        emit_event(
            event_type="call_error",
            phase=kind,
            payload={
                "kind": kind,
                "target": target,
                "duration_ms": elapsed_ms,
                "error": type(exc).__name__,
                "message": str(exc)[:400],
            },
        )
        raise


def _patch_asyncio() -> None:
    global _async_peak, _async_inflight
    original_create_task = asyncio.create_task

    def patched_create_task(coro: Any, *args: Any, **kwargs: Any) -> Any:
        nonlocal original_create_task
        global _async_inflight, _async_peak
        _async_inflight += 1
        _async_peak = max(_async_peak, _async_inflight)
        task = original_create_task(coro, *args, **kwargs)

        def _done_callback(_task: Any) -> None:
            global _async_inflight
            _async_inflight = max(0, _async_inflight - 1)

        task.add_done_callback(_done_callback)
        return task

    asyncio.create_task = patched_create_task


def _flush_summary() -> None:
    emit_event(
        event_type="runtime_summary",
        phase="runtime",
        payload={
            "thread_peak": _thread_peak,
            "process_peak": _process_peak,
            "async_peak": _async_peak,
        },
    )


_patch_asyncio()
atexit.register(_flush_summary)
