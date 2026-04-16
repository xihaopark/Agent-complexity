from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


_TRACE_MAX_TEXT = int(os.environ.get("TRACE_MAX_TEXT_CHARS", "20000"))
_TRACE_MAX_EVENTS = int(os.environ.get("TRACE_MAX_EVENTS", "200"))
_TRACE_INLINE_MAX_TEXT = int(os.environ.get("TRACE_INLINE_MAX_TEXT_CHARS", "4000"))
_TRACE_INLINE_MAX_EVENTS = int(os.environ.get("TRACE_INLINE_MAX_EVENTS", "20"))


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _truncate_text(value: str, max_len: int) -> str:
    if len(value) <= max_len:
        return value
    return value[:max_len] + "\n...[truncated]"


def json_safe(value: Any, *, max_text_len: int = _TRACE_MAX_TEXT) -> Any:
    if value is None or isinstance(value, (int, float, bool)):
        return value
    if isinstance(value, str):
        return _truncate_text(value, max_text_len)
    if isinstance(value, list):
        return [json_safe(item, max_text_len=max_text_len) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item, max_text_len=max_text_len) for item in value]
    if isinstance(value, dict):
        return {
            str(key): json_safe(item, max_text_len=max_text_len)
            for key, item in value.items()
        }
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return _truncate_text(str(value), max_text_len)


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    parts.append(text)
                else:
                    parts.append(json.dumps(json_safe(item), ensure_ascii=False))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part).strip()
    if isinstance(content, dict):
        text = content.get("text")
        if isinstance(text, str):
            return text
        return json.dumps(json_safe(content), ensure_ascii=False)
    return str(content or "")


def serialize_prompt_messages(messages: Iterable[Any]) -> List[Dict[str, Any]]:
    serialized: List[Dict[str, Any]] = []
    for message in messages:
        role = getattr(message, "type", "") or getattr(message, "role", "")
        if not role:
            role = message.__class__.__name__.replace("Message", "").lower()
        content = getattr(message, "content", message)
        serialized.append(
            {
                "role": role,
                "content": json_safe(content),
                "text": _truncate_text(_content_to_text(content), _TRACE_MAX_TEXT),
            }
        )
    return serialized


def serialize_llm_response(response: Any) -> Dict[str, Any]:
    if response is None:
        return {}

    content = getattr(response, "content", response)
    payload = {
        "id": getattr(response, "id", ""),
        "type": getattr(response, "type", ""),
        "content": json_safe(content),
        "text": _truncate_text(_content_to_text(content), _TRACE_MAX_TEXT),
        "additional_kwargs": json_safe(getattr(response, "additional_kwargs", {})),
        "response_metadata": json_safe(getattr(response, "response_metadata", {})),
        "usage_metadata": json_safe(getattr(response, "usage_metadata", {})),
        "tool_calls": json_safe(getattr(response, "tool_calls", [])),
        "invalid_tool_calls": json_safe(getattr(response, "invalid_tool_calls", [])),
    }
    return payload


def _as_int(value: Any) -> Optional[int]:
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_float(value: Any) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _lookup_nested(mapping: Any, *path: str) -> Any:
    current = mapping
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def infer_step_id(context: Optional[Dict[str, Any]]) -> str:
    if not isinstance(context, dict):
        return ""
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


def infer_workflow_id(context: Optional[Dict[str, Any]]) -> str:
    if not isinstance(context, dict):
        return ""
    for key in ("workflow_id", "workflow_id_requested"):
        value = context.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    workflow_ctx = context.get("workflow_run_context")
    if isinstance(workflow_ctx, dict):
        value = workflow_ctx.get("workflow_id")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_token_usage(response: Any) -> Dict[str, Any]:
    response_metadata = getattr(response, "response_metadata", {}) or {}
    usage_metadata = getattr(response, "usage_metadata", {}) or {}
    token_usage = response_metadata.get("token_usage")
    usage = response_metadata.get("usage")

    prompt_tokens = (
        _as_int(_lookup_nested(token_usage, "prompt_tokens"))
        or _as_int(_lookup_nested(usage, "prompt_tokens"))
        or _as_int(_lookup_nested(usage_metadata, "input_tokens"))
        or _as_int(_lookup_nested(usage_metadata, "prompt_tokens"))
    )
    completion_tokens = (
        _as_int(_lookup_nested(token_usage, "completion_tokens"))
        or _as_int(_lookup_nested(usage, "completion_tokens"))
        or _as_int(_lookup_nested(usage_metadata, "output_tokens"))
        or _as_int(_lookup_nested(usage_metadata, "completion_tokens"))
    )
    total_tokens = (
        _as_int(_lookup_nested(token_usage, "total_tokens"))
        or _as_int(_lookup_nested(usage, "total_tokens"))
        or _as_int(_lookup_nested(usage_metadata, "total_tokens"))
    )
    reasoning_tokens = (
        _as_int(_lookup_nested(token_usage, "completion_tokens_details", "reasoning_tokens"))
        or _as_int(_lookup_nested(token_usage, "output_token_details", "reasoning"))
        or _as_int(_lookup_nested(usage, "completion_tokens_details", "reasoning_tokens"))
        or _as_int(_lookup_nested(usage_metadata, "output_token_details", "reasoning"))
    )
    cost = (
        _as_float(_lookup_nested(token_usage, "cost"))
        or _as_float(_lookup_nested(usage, "cost"))
        or _as_float(_lookup_nested(response_metadata, "cost"))
        or _as_float(_lookup_nested(usage_metadata, "cost"))
    )

    normalized = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "reasoning_tokens": reasoning_tokens,
        "cost": cost,
    }
    if all(value in (None, 0, 0.0) for value in normalized.values()):
        return {}
    return normalized


def build_llm_trace_entry(
    *,
    node: str,
    purpose: str,
    prompt_messages: Iterable[Any],
    response: Any = None,
    status: str = "success",
    parsed_output: Any = None,
    error: str = "",
    context: Optional[Dict[str, Any]] = None,
    model: str = "",
) -> Dict[str, Any]:
    step_id = infer_step_id(context)
    workflow_id = infer_workflow_id(context)
    return {
        "trace_id": f"llm-{uuid.uuid4().hex[:12]}",
        "at": now_iso(),
        "node": node,
        "purpose": purpose,
        "status": status,
        "model": model,
        "workflow_id": workflow_id,
        "step_id": step_id,
        "prompt": serialize_prompt_messages(prompt_messages),
        "response": serialize_llm_response(response),
        "token_usage": extract_token_usage(response),
        "parsed_output": json_safe(parsed_output),
        "error": _truncate_text(error, _TRACE_MAX_TEXT) if error else "",
        "context": json_safe(context or {}),
    }


def build_orchestration_trace_entry(
    *,
    event_type: str,
    workflow_id: str = "",
    step_id: str = "",
    reason: str = "",
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "trace_id": f"orch-{uuid.uuid4().hex[:12]}",
        "at": now_iso(),
        "event_type": event_type,
        "workflow_id": workflow_id,
        "step_id": step_id,
        "reason": _truncate_text(reason, _TRACE_MAX_TEXT),
        "details": json_safe(details or {}),
    }


def append_trace(entries: Any, event: Dict[str, Any], *, max_events: int = _TRACE_MAX_EVENTS) -> List[Dict[str, Any]]:
    trace: List[Dict[str, Any]] = []
    if isinstance(entries, list):
        trace.extend(item for item in entries if isinstance(item, dict))
    trace.append(json_safe(event))
    return trace[-max_events:]


def compact_trace_entries(
    entries: Any,
    *,
    max_events: int = _TRACE_INLINE_MAX_EVENTS,
    max_text_len: int = _TRACE_INLINE_MAX_TEXT,
) -> List[Dict[str, Any]]:
    if not isinstance(entries, list):
        return []
    compacted: List[Dict[str, Any]] = []
    for raw in entries[-max_events:]:
        if not isinstance(raw, dict):
            continue
        compacted.append(json_safe(raw, max_text_len=max_text_len))
    return compacted
