#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", help="Comparison output dir that contains workdirs/agent/data")
    parser.add_argument("--data-root", help="Agent data root that contains experiments/")
    parser.add_argument("--session-dir", help="Concrete experiments/.../sessions/... directory to watch")
    parser.add_argument("--result-json", help="Optional result JSON path; stop once it exists")
    parser.add_argument("--poll-seconds", type=float, default=3.0)
    parser.add_argument("--response-chars", type=int, default=800)
    parser.add_argument("--show-prompt", action="store_true")
    return parser.parse_args(argv)


def resolve_data_root(args: argparse.Namespace) -> Path | None:
    if args.session_dir:
        return None
    if args.data_root:
        return Path(args.data_root).resolve()
    if args.output_dir:
        return (Path(args.output_dir).resolve() / "workdirs" / "agent" / "data").resolve()
    return None


def find_latest_session_dir(data_root: Path) -> Path | None:
    experiments_dir = data_root / "experiments"
    if not experiments_dir.exists():
        return None
    candidates = [
        path.parent
        for path in experiments_dir.glob("exp-*/sessions/sess-*/session.json")
        if path.is_file()
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: (path / "session.json").stat().st_mtime)


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def compact_text(value: Any, limit: int) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                text = item.get("content") or item.get("text") or ""
            else:
                text = str(item)
            if text:
                parts.append(str(text))
        value = "\n".join(parts)
    elif isinstance(value, dict):
        value = json.dumps(value, ensure_ascii=False)
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def print_orch_event(item: dict[str, Any]) -> None:
    at = item.get("at") or "?"
    event_type = item.get("event_type") or "?"
    step_id = item.get("step_id") or item.get("selected_step_id") or "-"
    reason = compact_text(item.get("reason"), 1200)
    print(f"[{at}] ORCH {event_type} step={step_id}")
    if reason:
        print(f"  reason: {reason}")
    details = item.get("details") or {}
    ready_steps = details.get("ready_steps") or []
    if ready_steps:
        ready_ids = ", ".join(str(step.get("id")) for step in ready_steps if step.get("id"))
        if ready_ids:
            print(f"  ready: {ready_ids}")
    sys.stdout.flush()


def print_llm_event(item: dict[str, Any], *, response_chars: int, show_prompt: bool) -> None:
    at = item.get("at") or "?"
    node = item.get("node") or "?"
    purpose = item.get("purpose") or "-"
    status = item.get("status") or "?"
    model = item.get("model") or "-"
    print(f"[{at}] LLM node={node} purpose={purpose} status={status} model={model}")
    if show_prompt:
        prompt = compact_text(item.get("prompt"), 1200)
        if prompt:
            print(f"  prompt: {prompt}")
    response_payload = item.get("response") or {}
    response = compact_text(
        response_payload.get("text")
        or item.get("raw_response_text")
        or item.get("parsed_response")
        or item.get("parsed_output")
        or item.get("error"),
        response_chars,
    )
    if response:
        print(f"  response: {response}")
    sys.stdout.flush()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result_json = Path(args.result_json).resolve() if args.result_json else None
    data_root = resolve_data_root(args)
    session_dir = Path(args.session_dir).resolve() if args.session_dir else None
    seen_orch: set[str] = set()
    seen_llm: set[str] = set()
    announced_session = False
    last_status = ""

    while True:
        if session_dir is None and data_root is not None:
            session_dir = find_latest_session_dir(data_root)
        if session_dir is not None and session_dir.exists():
            if not announced_session:
                print(f"Watching session: {session_dir}")
                sys.stdout.flush()
                announced_session = True

            orch_items = load_json(session_dir / "memory" / "state.orchestration_trace.json") or []
            for item in orch_items:
                trace_id = str(item.get("trace_id") or "")
                if not trace_id or trace_id in seen_orch:
                    continue
                seen_orch.add(trace_id)
                print_orch_event(item)

            llm_items = load_json(session_dir / "memory" / "state.llm_trace.json") or []
            for item in llm_items:
                trace_id = str(item.get("trace_id") or "")
                if not trace_id or trace_id in seen_llm:
                    continue
                seen_llm.add(trace_id)
                print_llm_event(item, response_chars=args.response_chars, show_prompt=args.show_prompt)

            session_obj = load_json(session_dir / "session.json") or {}
            workflow_status = (
                session_obj.get("workflow_status")
                or ((session_obj.get("agent_state") or {}).get("workflow_status"))
                or ""
            )
            if workflow_status and workflow_status != last_status:
                print(f"STATUS workflow_status={workflow_status}")
                sys.stdout.flush()
                last_status = workflow_status
                if workflow_status in {"success", "failed", "error"} and (result_json is None or result_json.exists()):
                    return 0

        if result_json is not None and result_json.exists() and announced_session:
            return 0
        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
