from __future__ import annotations

import os
import re
import sys
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


@dataclass
class _ResponseStub:
    content: str
    response_metadata: Dict[str, Any]
    usage_metadata: Dict[str, Any] = None


def _openrouter_chat(
    *,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    max_tokens: int = 1024,
    timeout: int = 180,
    headers: Optional[Dict[str, str]] = None,
) -> _ResponseStub:
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set.")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    merged_headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/renzo",
        "X-Title": "Renzo Workflow Selector",
    }
    if headers:
        merged_headers.update(headers)
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json=payload,
        headers=merged_headers,
        timeout=timeout,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter API error {resp.status_code}: {resp.text[:500]}")
    data = resp.json()
    content = (((data.get("choices") or [{}])[0]).get("message") or {}).get("content") or ""
    usage = data.get("usage") or {}
    response_metadata = {
        "token_usage": {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "cost": usage.get("cost"),
        },
        "usage": usage,
        "model": model,
    }
    return _ResponseStub(content=str(content), response_metadata=response_metadata, usage_metadata={})


def _normalize_step_id(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        return ""
    raw = raw.splitlines()[0].strip().strip('"').strip("'")
    m = re.search(r"[A-Za-z0-9][A-Za-z0-9_\-]*", raw)
    return m.group(0) if m else ""


def _default_selector_model() -> str:
    return (
        os.environ.get("WORKFLOW_STEP_SELECTOR_MODEL")
        or os.environ.get("LLM_MODEL")
        or os.environ.get("OPENROUTER_MODEL")
        or "deepseek/deepseek-v3.2-exp"
    )


_BIOMNI_A1: Any = None
_STELLA_MANAGER: Any = None
_STELLA_INIT_OK: Optional[bool] = None
_TOOLUNIVERSE_AGENTIC: dict[str, Any] = {}


def _maybe_init_biomni_a1(model: str) -> Any:
    global _BIOMNI_A1
    if _BIOMNI_A1 is not None:
        return _BIOMNI_A1
    try:
        from biomni.agent import A1
    except Exception:
        return None
    data_dir = os.environ.get("BIOMNI_DATA_DIR") or os.path.join(os.getcwd(), ".biomni_data")
    os.makedirs(data_dir, exist_ok=True)
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        _BIOMNI_A1 = A1(
            path=data_dir,
            llm=model,
            source="Custom",
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            use_tool_retriever=False,
            timeout_seconds=int(os.environ.get("BIOMNI_TIMEOUT_SECONDS", "120")),
            expected_data_lake_files=[],
        )
        return _BIOMNI_A1
    except Exception:
        return None


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _diagnostic_replay_block(agent_name: str) -> str:
    keys = [
        "WORKFLOW_DIAGNOSTIC_REPLAY_HINT",
        f"{(agent_name or '').strip().upper()}_DIAGNOSTIC_REPLAY_HINT",
    ]
    for key in keys:
        raw = os.environ.get(key, "").strip()
        if not raw:
            continue
        try:
            text = json.dumps(json.loads(raw), ensure_ascii=False)
        except Exception:
            text = raw
        return (
            "DIAGNOSTIC_REPLAY_HINT:\n"
            f"{text}\n"
            "Use this only as a recovery hint. Do not violate ready-step constraints or invent missing inputs."
        )
    return ""


def _ensure_stella_manager() -> Any:
    global _STELLA_MANAGER, _STELLA_INIT_OK
    if _STELLA_MANAGER is not None:
        return _STELLA_MANAGER

    stella_dir = (os.environ.get("STELLA_DIR") or "").strip()
    if stella_dir:
        if stella_dir not in sys.path:
            sys.path.insert(0, stella_dir)

    try:
        import stella_core
    except Exception:
        _STELLA_INIT_OK = False
        return None

    if _STELLA_INIT_OK is None:
        try:
            use_template = _truthy(os.environ.get("STELLA_USE_TEMPLATES", "0"))
            use_mem0 = _truthy(os.environ.get("STELLA_USE_MEM0", "0"))
            _STELLA_INIT_OK = bool(stella_core.initialize_stella(use_template=use_template, use_mem0=use_mem0))
        except Exception:
            _STELLA_INIT_OK = False

    if not _STELLA_INIT_OK:
        return None

    manager = getattr(stella_core, "manager_agent", None)
    if manager is None:
        return None
    _STELLA_MANAGER = manager
    return _STELLA_MANAGER


def _try_stella_smolagents_select(
    *,
    model: str,
    system: str,
    user: str,
) -> Optional[_ResponseStub]:
    manager = _ensure_stella_manager()
    if manager is None:
        return None
    try:
        prompt = f"{system}\n\n{user}\n\nOutput only the chosen step id."
        content = manager.run(prompt)
        return _ResponseStub(
            content=str(content),
            response_metadata={"model": model, "token_usage": {}},
            usage_metadata={},
        )
    except Exception:
        return None


def _maybe_init_tooluniverse_agentic(model: str) -> Any:
    cached = _TOOLUNIVERSE_AGENTIC.get(model)
    if cached is not None:
        return cached
    try:
        from tooluniverse.agentic_tool import AgenticTool
    except Exception:
        return None
    if not os.environ.get("OPENROUTER_API_KEY", "").strip():
        return None
    agentic_config = {
        "name": "FinishWorkflowStepSelector",
        "description": "ToolUniverse-backed selector for choosing the next ready finish workflow step.",
        "type": "AgenticTool",
        "prompt": (
            "You are ToolUniverse's AgenticTool acting as a workflow step selector.\n"
            "workflow_id={workflow_id}\n"
            "completed_steps={completed_steps}\n"
            "allowed_step_ids={allowed_step_ids}\n"
            "ready_steps={ready_steps}\n"
            "{diagnostic_replay_hint}\n"
            "Choose exactly one step id from allowed_step_ids.\n"
            "Prefer steps with explicit IO contracts and steps that keep the current workflow executable.\n"
            "Output only the chosen step id and nothing else."
        ),
        "input_arguments": [
            "workflow_id",
            "completed_steps",
            "allowed_step_ids",
            "ready_steps",
            "diagnostic_replay_hint",
        ],
        "parameter": {
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string"},
                "completed_steps": {"type": "string"},
                "allowed_step_ids": {"type": "string"},
                "ready_steps": {"type": "string"},
                "diagnostic_replay_hint": {"type": "string"},
            },
            "required": [
                "workflow_id",
                "completed_steps",
                "allowed_step_ids",
                "ready_steps",
                "diagnostic_replay_hint",
            ],
        },
        "configs": {
            "api_type": "OPENROUTER",
            "model_id": model,
            "temperature": 0.0,
            "return_json": False,
            "return_metadata": True,
            "validate_api_key": True,
            "use_global_fallback": False,
        },
    }
    try:
        selector = AgenticTool(agentic_config)
    except Exception:
        return None
    _TOOLUNIVERSE_AGENTIC[model] = selector
    return selector


def _try_tooluniverse_agentic_select(
    *,
    model: str,
    workflow_id: str,
    completed_step_ids: List[str],
    strict_allowed_ids: List[str],
    ready_steps: List[Dict[str, Any]],
    replay_block: str,
) -> Optional[_ResponseStub]:
    selector = _maybe_init_tooluniverse_agentic(model)
    if selector is None:
        return None
    try:
        payload = selector.run(
            {
                "workflow_id": workflow_id,
                "completed_steps": json.dumps(completed_step_ids, ensure_ascii=False),
                "allowed_step_ids": json.dumps(strict_allowed_ids, ensure_ascii=False),
                "ready_steps": json.dumps(ready_steps, ensure_ascii=False),
                "diagnostic_replay_hint": replay_block or "NO_DIAGNOSTIC_REPLAY_HINT",
            }
        )
    except Exception:
        return None
    if not isinstance(payload, dict) or not payload.get("success"):
        return None
    response_metadata = {"model": model, "token_usage": {}}
    metadata = payload.get("metadata")
    if isinstance(metadata, dict):
        response_metadata["tooluniverse_metadata"] = metadata
    return _ResponseStub(
        content=str(payload.get("result") or ""),
        response_metadata=response_metadata,
        usage_metadata={},
    )


def select_step_external(
    *,
    agent_name: str,
    workflow_id: str,
    ready_steps: List[Dict[str, Any]],
    completed_step_ids: List[str],
    strict_allowed_ids: List[str],
) -> Tuple[str, Dict[str, Any]]:
    name = (agent_name or "").strip().lower()
    model = _default_selector_model()
    replay_block = _diagnostic_replay_block(name)

    if name == "dswizard":
        plan_system = os.environ.get("DSWIZARD_PLAN_SYSTEM_PROMPT") or (
            "You are DSWizard's Plan Agent. You plan the next workflow step selection.\n"
            "Output must be wrapped in <analysis_plan>...</analysis_plan>.\n"
            "Do not output a final step id in this phase."
        )
        plan_user = (
            f"workflow_id={workflow_id}\n"
            f"completed_steps={completed_step_ids}\n"
            f"allowed_step_ids={strict_allowed_ids}\n"
            f"ready_steps={ready_steps}\n"
            "Create a short plan to decide which ready step to execute next."
        )
        plan_resp = _openrouter_chat(
            model=model,
            messages=[{"role": "system", "content": plan_system}, {"role": "user", "content": plan_user}],
            temperature=0.2,
            max_tokens=800,
            headers={"X-Title": "DSWizard-StepSelection"},
        )
        plan_text = plan_resp.content or ""
        m = re.search(r"<analysis_plan>(.*?)</analysis_plan>", plan_text, re.DOTALL | re.IGNORECASE)
        extracted_plan = (m.group(1).strip() if m else plan_text.strip())[:4000]

        choose_system = os.environ.get("DSWIZARD_CODE_SYSTEM_PROMPT") or (
            "You are DSWizard's Code Agent, but for this task you must output ONLY the chosen step id.\n"
            "Choose exactly one id from the allowed set and output only that id."
        )
        choose_user = (
            f"workflow_id={workflow_id}\n"
            f"completed_steps={completed_step_ids}\n"
            f"allowed_step_ids={strict_allowed_ids}\n"
            f"ready_steps={ready_steps}\n"
            f"ANALYSIS_PLAN:\n{extracted_plan}\n"
            "Output the chosen step id only."
        )
        choose_resp = _openrouter_chat(
            model=model,
            messages=[{"role": "system", "content": choose_system}, {"role": "user", "content": choose_user}],
            temperature=0.0,
            max_tokens=50,
            headers={"X-Title": "DSWizard-StepSelection"},
        )
        step_id = _normalize_step_id(choose_resp.content)
        if step_id not in set(strict_allowed_ids):
            step_id = ""
        trace = {
            "prompt_messages": [
                {"role": "system", "content": plan_system},
                {"role": "user", "content": plan_user},
                {"role": "assistant", "content": plan_resp.content},
                {"role": "system", "content": choose_system},
                {"role": "user", "content": choose_user},
            ],
            "response": choose_resp,
            "model": model,
            "parsed_output": {"selected_step_id": step_id, "phase": "plan_then_choose"},
        }
        return step_id, trace

    if name == "tooluniverse":
        system = os.environ.get("TOOLUNIVERSE_SYSTEM_PROMPT") or (
            "You are ToolUniverse. Select the next workflow step to execute.\n"
            "Choose exactly one step id from the allowed set and output only that id."
        )
        user = (
            f"workflow_id={workflow_id}\n"
            f"completed_steps={completed_step_ids}\n"
            f"allowed_step_ids={strict_allowed_ids}\n"
            f"ready_steps={ready_steps}\n"
            f"{replay_block}\n"
        )
        require_framework = _truthy(os.environ.get("REQUIRE_REAL_AGENT_FRAMEWORK", "0"))
        resp = _try_tooluniverse_agentic_select(
            model=model,
            workflow_id=workflow_id,
            completed_step_ids=completed_step_ids,
            strict_allowed_ids=strict_allowed_ids,
            ready_steps=ready_steps,
            replay_block=replay_block,
        )
        if resp is None and not require_framework:
            resp = _openrouter_chat(
                model=model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.0,
                max_tokens=80,
                headers={"X-Title": "ToolUniverse-StepSelection"},
            )
        if resp is None:
            return "", {
                "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "response": None,
                "model": model,
                "parsed_output": {"selected_step_id": "", "error": "tooluniverse_framework_unavailable", "replay_hint_present": bool(replay_block)},
            }
        step_id = _normalize_step_id(resp.content)
        if step_id not in set(strict_allowed_ids):
            step_id = ""
        trace = {
            "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "response": resp,
            "model": model,
            "parsed_output": {"selected_step_id": step_id, "replay_hint_present": bool(replay_block)},
        }
        return step_id, trace

    if name == "biomni":
        system = os.environ.get("BIOMNI_SYSTEM_PROMPT") or (
            "You are Biomni (A1-style). Select the next workflow step to execute.\n"
            "Choose exactly one step id from the allowed set and output only that id.\n"
            "If a diagnostic replay hint is provided, use it to avoid repeating known failure modes, "
            "but never violate the ready-step set."
        )
        user = (
            f"workflow_id={workflow_id}\n"
            f"completed_steps={completed_step_ids}\n"
            f"allowed_step_ids={strict_allowed_ids}\n"
            f"ready_steps={ready_steps}\n"
            f"{replay_block}\n"
        )
        require_framework = _truthy(os.environ.get("REQUIRE_REAL_AGENT_FRAMEWORK", "0"))
        a1 = _maybe_init_biomni_a1(model)
        if a1 is not None:
            try:
                _, final_response = a1.go(f"{system}\n\n{user}\n")
                resp = _ResponseStub(content=str(final_response), response_metadata={"model": model, "token_usage": {}}, usage_metadata={})
            except Exception:
                if require_framework:
                    return "", {
                        "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                        "response": None,
                        "model": model,
                        "parsed_output": {"selected_step_id": "", "error": "biomni_a1_failed", "replay_hint_present": bool(replay_block)},
                    }
                resp = _openrouter_chat(
                    model=model,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    temperature=0.0,
                    max_tokens=80,
                    headers={"X-Title": "Biomni-StepSelection"},
                )
        else:
            if require_framework:
                return "", {
                    "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                    "response": None,
                    "model": model,
                    "parsed_output": {"selected_step_id": "", "error": "biomni_framework_unavailable", "replay_hint_present": bool(replay_block)},
                }
            resp = _openrouter_chat(
                model=model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.0,
                max_tokens=80,
                headers={"X-Title": "Biomni-StepSelection"},
            )
        step_id = _normalize_step_id(resp.content)
        if step_id not in set(strict_allowed_ids):
            step_id = ""
        trace = {
            "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "response": resp,
            "model": model,
            "parsed_output": {"selected_step_id": step_id, "replay_hint_present": bool(replay_block)},
        }
        return step_id, trace

    if name == "stella":
        system = os.environ.get("STELLA_SYSTEM_PROMPT") or (
            "You are STELLA. Select the next workflow step to execute.\n"
            "Choose exactly one step id from the allowed set and output only that id."
        )
        user = (
            f"workflow_id={workflow_id}\n"
            f"completed_steps={completed_step_ids}\n"
            f"allowed_step_ids={strict_allowed_ids}\n"
            f"ready_steps={ready_steps}\n"
            f"{replay_block}\n"
        )
        require_framework = _truthy(os.environ.get("REQUIRE_REAL_AGENT_FRAMEWORK", "0"))
        resp = _try_stella_smolagents_select(model=model, system=system, user=user)
        if resp is None and not require_framework:
            resp = _openrouter_chat(
                model=model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.0,
                max_tokens=80,
                headers={"X-Title": "STELLA-StepSelection"},
            )
        if resp is None:
            return "", {
                "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "response": None,
                "model": model,
                "parsed_output": {"selected_step_id": "", "error": "stella_framework_unavailable", "replay_hint_present": bool(replay_block)},
            }
        step_id = _normalize_step_id(resp.content)
        if step_id not in set(strict_allowed_ids):
            step_id = ""
        trace = {
            "prompt_messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "response": resp,
            "model": model,
            "parsed_output": {"selected_step_id": step_id, "replay_hint_present": bool(replay_block)},
        }
        return step_id, trace

    return "", {"prompt_messages": [], "response": None, "model": model, "parsed_output": {"selected_step_id": ""}}
