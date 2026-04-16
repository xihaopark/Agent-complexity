from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from renzo.app.shell.schema import ShellDecision


class ShellToolRouter:
    """Routes structured shell tool calls to backend capabilities."""

    def __init__(
        self,
        *,
        list_workflows: Callable[[], List[Dict[str, Any]]],
        get_workflow: Callable[[str], Optional[Dict[str, Any]]],
        create_workflow: Callable[..., Dict[str, Any]],
        start_experiment_from_workflow: Callable[[str, Dict[str, Any]], Dict[str, Any]],
        list_datasets: Callable[[], List[Dict[str, Any]]],
        link_experiment: Callable[[str, Dict[str, Any]], Optional[Dict[str, Any]]],
    ) -> None:
        self._list_workflows = list_workflows
        self._get_workflow = get_workflow
        self._create_workflow = create_workflow
        self._start_experiment_from_workflow = start_experiment_from_workflow
        self._list_datasets = list_datasets
        self._link_experiment = link_experiment

    def execute(
        self,
        *,
        decision: ShellDecision,
        session: Dict[str, Any],
        context: Dict[str, Any],
        action_edits: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        tool_results: List[Dict[str, Any]] = []
        run_engine_prompt = None

        edits = action_edits or {}

        for call in decision.tool_calls:
            name = call.name
            args = dict(call.arguments or {})
            if name == "run_engine_turn":
                run_engine_prompt = str(
                    edits.get("engine_prompt")
                    or args.get("prompt")
                    or "Start the linked workflow and execute the first step."
                )
                tool_results.append({"tool": name, "ok": True, "result": {"prompt": run_engine_prompt}})
                continue

            if name == "engine_control":
                command = str(edits.get("command") or args.get("command") or "continue").strip().lower()
                prompt_map = {
                    "continue": "continue",
                    "pause": None,
                    "stop": "stop this workflow run and summarize current status.",
                    "retry_step": f"retry current step {args.get('target_step_id') or ''}".strip(),
                    "backtrack_step": f"go back to previous step and rerun from there {args.get('target_step_id') or ''}".strip(),
                    "reset_to_step": "continue",
                }
                run_engine_prompt = prompt_map.get(command)
                tool_results.append({
                    "tool": name,
                    "ok": True,
                    "result": {"command": command, "prompt": run_engine_prompt},
                })
                continue

            try:
                if name == "list_workflows":
                    workflows = self._list_workflows() or []
                    compact = [
                        {
                            "id": w.get("id"),
                            "name": w.get("name"),
                            "engine": w.get("engine"),
                            "description": w.get("description", ""),
                        }
                        for w in workflows[:20]
                    ]
                    tool_results.append({"tool": name, "ok": True, "result": compact})
                elif name == "get_workflow":
                    wf_id = str(args.get("workflow_id") or context.get("linked_workflow_id") or "").strip()
                    if not wf_id:
                        raise ValueError("workflow_id is required")
                    wf = self._get_workflow(wf_id)
                    tool_results.append({"tool": name, "ok": bool(wf), "result": wf})
                elif name == "create_workflow":
                    payload = {
                        "name": str(args.get("name") or edits.get("name") or "New workflow"),
                        "engine": str(args.get("engine") or "agent"),
                        "description": str(args.get("description") or "Created by Shell"),
                        "steps": args.get("steps") or [],
                        "know_how_content": args.get("know_how_content"),
                        "input_hints": args.get("input_hints") or [],
                        "output_hints": args.get("output_hints") or [],
                    }
                    wf = self._create_workflow(**payload)
                    tool_results.append({"tool": name, "ok": True, "result": wf})
                elif name == "start_experiment_from_workflow":
                    wf_id = str(args.get("workflow_id") or context.get("linked_workflow_id") or "").strip()
                    if not wf_id:
                        raise ValueError("workflow_id is required")
                    req = {
                        "name": str(args.get("name") or edits.get("name") or ""),
                        "dataset_ids": args.get("dataset_ids") or None,
                    }
                    out = self._start_experiment_from_workflow(wf_id, req)
                    tool_results.append({"tool": name, "ok": True, "result": out})
                elif name == "list_datasets":
                    scope = str(args.get("scope") or "linked").strip().lower()
                    linked_ids = [str(x) for x in (context.get("linked_dataset_ids") or []) if x]
                    linked_id_set = set(linked_ids)
                    datasets = self._list_datasets() or []
                    if scope in {"linked", "experiment", "session"} and linked_ids:
                        datasets = [d for d in datasets if str(d.get("id") or "") in linked_id_set]
                    compact = [
                        {
                            "id": d.get("id"),
                            "name": d.get("name"),
                            "file_count": d.get("file_count", 0),
                            "description": d.get("description", ""),
                            "linked": str(d.get("id") or "") in linked_id_set,
                        }
                        for d in datasets[:30]
                    ]
                    tool_results.append({"tool": name, "ok": True, "result": compact})
                elif name == "link_experiment":
                    exp_id = str(args.get("experiment_id") or session.get("experiment_id") or "").strip()
                    if not exp_id:
                        raise ValueError("experiment_id is required")
                    updates: Dict[str, Any] = {}
                    if args.get("workflow_id"):
                        updates["workflow_id"] = args.get("workflow_id")
                    if args.get("dataset_ids") is not None:
                        updates["dataset_ids"] = args.get("dataset_ids")
                    if not updates:
                        raise ValueError("No updates provided")
                    out = self._link_experiment(exp_id, updates)
                    tool_results.append({"tool": name, "ok": bool(out), "result": out})
                else:
                    tool_results.append({"tool": name, "ok": False, "error": "Unsupported tool"})
            except Exception as exc:
                tool_results.append({"tool": name, "ok": False, "error": str(exc)})

        return {
            "tool_results": tool_results,
            "run_engine_prompt": run_engine_prompt,
        }
