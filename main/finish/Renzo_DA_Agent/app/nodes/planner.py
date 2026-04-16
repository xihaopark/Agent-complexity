"""planner node — central decision maker for the agent.

Responsibilities:
  1. Detect workflow intent and delegate to workflow plan creation.
  2. For general analysis: call LLM to create a multi-step plan (JSON).
  3. On QC/validation failure: call LLM to revise the plan (rolling revision).
  4. Route to the correct next node based on current plan state.
"""
from __future__ import annotations

import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from langchain_core.messages import HumanMessage, SystemMessage

from renzo.app.state import AgentState
from renzo.app.llm import get_llm
from renzo.app.knowhow import find_workflow_skill_specs
from renzo.app.nodes.data_analyst import build_catalog_summary
from renzo.app.error_patterns import format_error_book_lessons, query_error_book
from renzo.app.tracing import (
    append_trace,
    build_llm_trace_entry,
    build_orchestration_trace_entry,
)
from renzo.app.orchestration.step_selector_agents import select_step_external
from renzo.app.orchestration.plan_lifecycle import (
    init_plan,
    parse_plan_json,
    select_next_step,
)
from renzo.app.workflows import discover_workflows, get_workflow_by_id
from renzo.app.models.workflow_step import (
    WorkflowPlan, WorkflowStep, StepStatus, WorkflowEngine, StepMode,
)
from renzo.app.experiments import resolve_execution_workdir
from renzo.app.runners.snakemake_runner import SnakemakeRunner
from renzo.app.runners.nextflow_runner import NextflowRunner

logger = logging.getLogger(__name__)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _inject_error_book_lessons_into_goal(
    step_goal: str,
    *,
    error_book: List[Dict[str, Any]],
    workflow_id: str,
) -> str:
    """Enrich step goal with relevant session error lessons before coding."""
    if not error_book:
        return step_goal
    query_text = f"{workflow_id} {step_goal}"
    lessons = query_error_book(
        error_book=error_book,
        query_text=query_text,
        language="both",
        limit=4,
    )
    rendered = format_error_book_lessons(lessons, max_items=3)
    if not rendered:
        return step_goal
    return (
        f"{step_goal}\n\n"
        f"{rendered}\n"
        "MANDATORY: apply these lessons while designing code for this step."
    )

# ── Prompt templates ──────────────────────────────────────────────────

_PLAN_SYSTEM_PROMPT = """\
You are a data analysis planning agent. Your job is to create a step-by-step
analysis plan as a JSON array.
IMPORTANT: Always use English for all descriptions and text, regardless of the user's input language.

Each step must have these fields:
  - "id": a short unique identifier (e.g. "step_1", "clean_data")
  - "description": what this step does, in enough detail for execution (1-3 sentences; keep full—UI shows title + expandable details)
  - "type": one of "data_prep", "analysis", "visualization", "qc", "sdtm", "adam", "tlf", "validation"
  - "depends_on": list of step ids that must complete first (can be empty)
  - "language": (optional) "python" or "r" — preferred language for this step

Rules:
  - Always start with a data_prep step if data hasn't been profiled yet.
  - Always include at least one analysis step.
  - Include a visualization step if the user's goal implies visual outputs.
  - For clinical trial / CDISC tasks, use step types: "sdtm", "adam", "tlf", "validation".
    Do NOT set the "language" field unless the step absolutely requires a specific
    language (e.g. admiral derive_vars_* must use R). Let the code generator decide
    the best language automatically. Most data reading, profiling, merging, and QC
    tasks work better in Python/pandas.
  - Keep plan length reasonable: 3-8 steps for typical analyses; each step's description should be detailed enough for execution (the frontend shows a short title and expandable full text).
  - Use type "hitl" for key decisions where the user should choose (e.g. which ADaM
    datasets to create: ADSL only vs ADLB/ADAE, or scope/options that were not specified).
    Include a "question" field with a short, clear question. Do NOT add hitl for every
    request; only when there is a meaningful open choice. If the user already specified
    everything (data paths, analysis type, output format), do NOT add hitl. When in
    doubt on small details, proceed without asking.
  - Output ONLY the JSON array, no other text.

Example output:
[
  {"id": "step_1", "description": "Load and profile the dataset", "type": "data_prep", "depends_on": []},
  {"id": "step_2", "description": "Clean missing values and normalize columns", "type": "data_prep", "depends_on": ["step_1"]},
  {"id": "step_3", "description": "Run statistical analysis", "type": "analysis", "depends_on": ["step_2"]},
  {"id": "step_4", "description": "Generate summary visualizations", "type": "visualization", "depends_on": ["step_3"]}
]

Clinical trial example:
[
  {"id": "load_sdtm", "description": "Load SDTM datasets (DM, AE, EX, VS, LB) and profile", "type": "data_prep", "depends_on": []},
  {"id": "derive_adsl", "description": "Derive ADSL from DM/EX/DS/VS", "type": "adam", "depends_on": ["load_sdtm"]},
  {"id": "derive_adae", "description": "Derive ADAE from AE/ADSL", "type": "adam", "depends_on": ["derive_adsl"]},
  {"id": "create_demog_table", "description": "Create demographics TLF table", "type": "tlf", "depends_on": ["derive_adsl"]},
  {"id": "validate", "description": "Run validation checks on derived datasets", "type": "validation", "depends_on": ["derive_adsl", "derive_adae"]}
]
"""

_REPLAN_SYSTEM_PROMPT = """\
You are a data analysis planning agent. A previous plan step has failed or
produced poor quality results. Your job is to revise the plan.

You will receive:
  - The original goal
  - The current plan (with step statuses)
  - The validation/QC failure details

Respond with a revised JSON array of steps. You may:
  - Add new steps to fix the issue
  - Modify existing pending steps
  - Remove steps that are no longer needed

Keep completed steps as-is (don't change their status).
Output ONLY the JSON array, no other text.
"""


# ── Workflow intent detection (unchanged) ─────────────────────────────

def _detect_workflow_intent(state: AgentState) -> Optional[str]:
    """Check last user message for workflow run intent."""
    messages = state.get("messages") or []
    if not messages:
        return None
    last = messages[-1]
    content = getattr(last, "content", None) or str(last)
    if not isinstance(content, str):
        return None
    content = content.lower().strip()
    m = re.search(r"(?:run|execute)\s+(?:workflow\s+)?(\d+|\w+)", content, re.I)
    if m:
        candidate = m.group(1)
        wfs = discover_workflows()
        for w in wfs:
            if w.id == candidate or candidate.lower() in (w.name or "").lower():
                return w.id
        if candidate.isdigit():
            return candidate
    if "metataxonx" in content or "meta taxon" in content:
        for w in discover_workflows():
            if "meta" in (w.name or "").lower() and "taxon" in (w.name or "").lower():
                return w.id
    return None


def _populate_implicit_input_refs(steps: List[WorkflowStep]) -> None:
    by_id = {step.id: step for step in steps}
    for step in steps:
        if step.input_refs:
            continue
        inferred_refs: List[str] = []
        for dep_id in step.depends_on:
            dep = by_id.get(dep_id)
            if not dep:
                continue
            inferred_refs.extend(str(ref) for ref in [*dep.outputs, *dep.artifacts] if str(ref).strip())
        if inferred_refs:
            step.input_refs = list(dict.fromkeys(inferred_refs))


def _annotate_generic_plan_steps(
    steps: List[Dict[str, Any]],
    *,
    planning_source: str,
) -> List[Dict[str, Any]]:
    annotated: List[Dict[str, Any]] = []
    for index, raw in enumerate(steps, start=1):
        step = dict(raw)
        deps = [str(dep) for dep in (step.get("depends_on") or []) if str(dep).strip()]
        reason_parts = [f"Step {index} in the {planning_source} plan."]
        if deps:
            reason_parts.append("Declared upstream dependencies: " + ", ".join(deps) + ".")
        else:
            reason_parts.append("No upstream dependencies were declared.")
        if step.get("type"):
            reason_parts.append(f"Step type: {step['type']}.")
        step.setdefault("planning_source", planning_source)
        step.setdefault("orchestration_reason", " ".join(reason_parts))
        annotated.append(step)
    return annotated


def _workflow_step_reason(
    *,
    planning_source: str,
    description: str,
    depends_on: List[str],
    outputs: List[str],
    extra: Optional[List[str]] = None,
) -> str:
    parts = [f"Planning source: {planning_source}.", f"Step purpose: {description}."]
    if depends_on:
        parts.append("Runs after: " + ", ".join(depends_on) + ".")
    else:
        parts.append("Entry step because it has no upstream dependencies.")
    if outputs:
        parts.append("Expected outputs: " + ", ".join(outputs) + ".")
    if extra:
        parts.extend(item for item in extra if item)
    return " ".join(parts)


def _ready_step_details(plan: WorkflowPlan, *, strict_manifest: bool) -> List[Dict[str, Any]]:
    details: List[Dict[str, Any]] = []
    for step in plan.ready_steps(strict_manifest=strict_manifest):
        detail = {
            "id": step.id,
            "depends_on": list(step.depends_on),
            "outputs": list(step.outputs),
            "planning_source": step.planning_source,
            "orchestration_reason": step.orchestration_reason or "",
        }
        if not strict_manifest:
            detail["downstream_unlock_score"] = plan._downstream_unlock_score(step.id)
        details.append(detail)
    return details


def _workflow_selection_reason(
    plan: WorkflowPlan,
    step: WorkflowStep,
    *,
    strict_manifest: bool,
) -> str:
    if strict_manifest:
        return (
            f"Selected '{step.id}' because it is the first ready step under strict dependency order. "
            f"{step.orchestration_reason or ''}".strip()
        )
    unlock_score = plan._downstream_unlock_score(step.id)
    return (
        f"Selected '{step.id}' from the ready set using skills-only ranking: "
        f"downstream_unlock_score={unlock_score}, outputs={len(step.outputs)}, "
        f"dependency_count={len(step.depends_on)}. {step.orchestration_reason or ''}"
    ).strip()


def _parse_llm_selected_step_id(text: str, *, allowed: set[str]) -> str:
    raw = (text or "").strip()
    if not raw:
        return ""
    if raw.startswith("{") and raw.endswith("}"):
        try:
            obj = json.loads(raw)
            candidate = str(obj.get("id") or "").strip()
            return candidate if candidate in allowed else ""
        except Exception:
            return ""
    candidate = raw.splitlines()[0].strip().strip('"').strip("'")
    return candidate if candidate in allowed else ""


def _select_workflow_step_via_llm(
    plan: WorkflowPlan,
    ready_steps: List[WorkflowStep],
    *,
    workflow_id: str,
) -> Tuple[Optional[str], Dict[str, Any]]:
    prompt_messages: List[Any] = []
    llm = None
    try:
        allowed = {step.id for step in ready_steps}
        ready_payload = [
            {
                "id": step.id,
                "description": step.description,
                "depends_on": list(step.depends_on),
                "outputs": list(step.outputs),
                "planning_source": step.planning_source,
                "orchestration_reason": step.orchestration_reason or "",
            }
            for step in ready_steps
        ]
        selector_agent = os.environ.get("WORKFLOW_STEP_SELECTOR_AGENT", "").strip().lower()
        if selector_agent and selector_agent != "renzo":
            selected, selector_trace = select_step_external(
                agent_name=selector_agent,
                workflow_id=workflow_id,
                ready_steps=ready_payload,
                completed_step_ids=[str(x) for x in plan.completed_step_ids()],
                strict_allowed_ids=sorted(list(allowed)),
            )
            context = {"workflow_id": workflow_id, "step_id": selected or ""}
            trace_entry = build_llm_trace_entry(
                node="planner",
                purpose="select_workflow_step",
                prompt_messages=selector_trace.get("prompt_messages") or [],
                response=selector_trace.get("response"),
                status="success" if selected else "parse_failed",
                parsed_output={
                    "selected_step_id": selected,
                    "allowed_step_ids": sorted(list(allowed)),
                    "selector_agent": selector_agent,
                    "selector_mode": "external",
                    "phase": (selector_trace.get("parsed_output") or {}).get("phase") if isinstance(selector_trace.get("parsed_output"), dict) else "",
                },
                context=context,
                model=str(selector_trace.get("model") or ""),
            )
            return (selected or None), trace_entry

        llm = get_llm(temperature=0)
        system_prompt = os.environ.get("WORKFLOW_STEP_SELECTION_SYSTEM_PROMPT") or (
            "You are an orchestration agent selecting the next workflow step to execute. "
            "Choose exactly one step id from the allowed set and output only that id. "
            "Do not add any explanation or extra text. "
            "If there is only one ready step, output its id."
        )
        user_msg = (
            f"workflow_id={workflow_id}\n"
            f"completed_steps={json.dumps(plan.completed_step_ids(), ensure_ascii=False)}\n"
            f"allowed_step_ids={json.dumps(sorted(list(allowed)), ensure_ascii=False)}\n"
            f"ready_steps={json.dumps(ready_payload, ensure_ascii=False)}\n"
        )
        prompt_messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_msg),
        ]
        response = llm.invoke(prompt_messages)
        selected = _parse_llm_selected_step_id(response.content, allowed=allowed)
        context = {"workflow_id": workflow_id}
        if selected:
            context["step_id"] = selected
        trace_entry = build_llm_trace_entry(
            node="planner",
            purpose="select_workflow_step",
            prompt_messages=prompt_messages,
            response=response,
            status="success" if selected else "parse_failed",
            parsed_output={"selected_step_id": selected, "allowed_step_ids": sorted(list(allowed))},
            context=context,
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )
        return (selected or None), trace_entry
    except Exception as e:
        return None, build_llm_trace_entry(
            node="planner",
            purpose="select_workflow_step",
            prompt_messages=prompt_messages,
            response=None,
            status="error",
            parsed_output=None,
            error=str(e),
            context={"workflow_id": workflow_id},
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )


def _workflow_plan_created_event(
    plan: WorkflowPlan,
    *,
    mode: str,
    skills_only: bool,
) -> Dict[str, Any]:
    return build_orchestration_trace_entry(
        event_type="workflow_plan_created",
        workflow_id=plan.workflow_id,
        reason=(
            f"Created workflow plan in mode={mode}. "
            f"skills_only={skills_only}. step_count={len(plan.steps)}."
        ),
        details={
            "plan_id": plan.id,
            "workflow_dir": plan.workflow_dir,
            "work_dir": plan.work_dir,
            "steps": [
                {
                    "id": step.id,
                    "planning_source": step.planning_source,
                    "orchestration_reason": step.orchestration_reason,
                    "depends_on": list(step.depends_on),
                    "outputs": list(step.outputs),
                }
                for step in plan.steps
            ],
        },
    )


def _workflow_step_selected_event(
    plan: WorkflowPlan,
    step: WorkflowStep,
    *,
    strict_manifest: bool,
    stage: str,
) -> Dict[str, Any]:
    return build_orchestration_trace_entry(
        event_type="workflow_step_selected",
        workflow_id=plan.workflow_id,
        step_id=step.id,
        reason=_workflow_selection_reason(plan, step, strict_manifest=strict_manifest),
        details={
            "stage": stage,
            "strict_manifest": strict_manifest,
            "ready_steps": _ready_step_details(plan, strict_manifest=strict_manifest),
            "current_step_id": plan.current_step_id,
        },
    )


def _generic_plan_created_event(
    *,
    goal: str,
    planning_source: str,
    plan_steps: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return build_orchestration_trace_entry(
        event_type="generic_plan_created",
        reason=(
            f"Created a generic plan via {planning_source}. "
            f"step_count={len(plan_steps)}."
        ),
        details={
            "goal": goal[:500],
            "step_ids": [step.get("id") for step in plan_steps],
            "steps": [
                {
                    "id": step.get("id"),
                    "depends_on": step.get("depends_on", []),
                    "planning_source": step.get("planning_source"),
                    "orchestration_reason": step.get("orchestration_reason"),
                }
                for step in plan_steps
            ],
        },
    )


def _skills_only_mode(run_ctx: Dict[str, Any]) -> bool:
    return bool(
        run_ctx.get("skills_only")
        or run_ctx.get("orchestration_mode") == "skills_only"
        or run_ctx.get("manifest_step_graph_allowed") is False
    )


def _workflow_local_path_from_skill_path(path: str, workflow_id: str) -> str:
    normalized = str(path or "").strip().replace("\\", "/")
    prefix = f"finish/{workflow_id}/"
    if normalized.startswith(prefix):
        return normalized[len(prefix):]
    marker = f"/{prefix}"
    if marker in normalized:
        return normalized.split(marker, 1)[1]
    return normalized.lstrip("./")


def _create_skill_only_snakemake_steps(
    workflow_id: str,
    *,
    skills_dir: Optional[str],
) -> List[WorkflowStep]:
    specs = find_workflow_skill_specs(workflow_id, base_dir=skills_dir)
    steps: List[WorkflowStep] = []
    for spec in specs:
        snakefile = _workflow_local_path_from_skill_path(spec.step_file, workflow_id)
        params: Dict[str, Any] = {
            "run_directory": ".",
            "cores": 1,
            "use_conda": False,
        }
        if snakefile:
            params["snakefile"] = snakefile
        configfile = _workflow_local_path_from_skill_path(spec.config_file, workflow_id)
        if configfile:
            params["configfile"] = configfile
        if spec.shared_environment:
            params["shared_conda_env"] = spec.shared_environment
        reason_bits = []
        if spec.source_path:
            reason_bits.append(f"Skill file: {spec.source_path}.")
        if spec.step_file:
            reason_bits.append(f"Step file: {spec.step_file}.")
        if spec.execution_targets:
            reason_bits.append("Execution targets: " + ", ".join(spec.execution_targets) + ".")
        if spec.representative_outputs:
            reason_bits.append("Representative outputs: " + ", ".join(spec.representative_outputs) + ".")
        if spec.guardrails:
            reason_bits.append("Guardrails: " + " ".join(spec.guardrails))
        steps.append(
            WorkflowStep(
                id=spec.step_id,
                description=spec.step_name or spec.description or spec.step_id,
                engine=WorkflowEngine.SNAKEMAKE,
                targets=["all"],
                params=params,
                outputs=spec.completion_artifacts,
                depends_on=spec.upstream_requirements,
                max_retries=0,
                timeout=3600,
                planning_source="workflow_skill",
                orchestration_reason=_workflow_step_reason(
                    planning_source="workflow_skill",
                    description=spec.step_name or spec.description or spec.step_id,
                    depends_on=spec.upstream_requirements,
                    outputs=spec.completion_artifacts,
                    extra=reason_bits,
                ),
            )
        )
    return steps


def _create_workflow_plan(workflow_id: str, state: AgentState) -> Optional[WorkflowPlan]:
    """Create a stepwise execution plan for a workflow."""
    wf = get_workflow_by_id(workflow_id)
    if not wf:
        return None
    # wf.path may be a directory (unpacked crate) or a file (main.nf / .zip)
    wf_path = Path(wf.path) if wf.path else None
    if wf_path and wf_path.is_dir():
        workflow_dir = wf_path
    elif wf_path and wf_path.is_file():
        workflow_dir = wf_path.parent
    else:
        # Fallback: try workflow_pool/<id>
        pool_dir = Path(os.getcwd()) / "workflow_pool" / workflow_id
        if pool_dir.exists():
            workflow_dir = pool_dir
        else:
            return None
    run_ctx = dict(state.get("workflow_run_context") or {})
    run_id = run_ctx.get("run_id") or f"wf-{workflow_id}-{uuid.uuid4().hex[:8]}"
    work_dir = Path(
        state.get("execution_workdir")
        or resolve_execution_workdir(
            state.get("experiment_id"),
            state.get("session_id"),
            state.get("artifact_policy", "session"),
        )
    )
    work_dir.mkdir(parents=True, exist_ok=True)

    # Determine engine type
    engine_str = (wf.engine or "").lower()
    steps: List[WorkflowStep] = []
    skills_only = _skills_only_mode(run_ctx)
    skills_dir = os.environ.get("WORKFLOW_SKILLS_DIR", "").strip() or None

    if engine_str == "agent":
        # Agent-driven workflow: build steps from manifest step definitions
        manifest_steps = wf.steps or []
        for i, ms in enumerate(manifest_steps):
            step_id = ms.get("id", f"step-{i+1}")
            steps.append(WorkflowStep(
                id=step_id,
                description=ms.get("name", ms.get("description", f"Step {i+1}")),
                engine=WorkflowEngine.AGENT,
                mode=ms.get("mode", StepMode.AGENT_CODE.value),
                prompt_hint=ms.get("prompt_hint"),
                hitl=ms.get("hitl"),
                input_refs=ms.get("input_refs", []),
                output_type=ms.get("output_type"),
                outputs=ms.get("outputs") or [],
                depends_on=ms.get("depends_on", []),
                planning_source="workflow_manifest",
                orchestration_reason=_workflow_step_reason(
                    planning_source="workflow_manifest",
                    description=ms.get("name", ms.get("description", f"Step {i+1}")),
                    depends_on=ms.get("depends_on", []),
                    outputs=ms.get("outputs") or [],
                ),
            ))
        logger.info("Created agent workflow plan with %d steps for %s", len(steps), workflow_id)
    elif engine_str == "snakemake":
        engine = WorkflowEngine.SNAKEMAKE
        if skills_only:
            steps = _create_skill_only_snakemake_steps(
                workflow_id,
                skills_dir=skills_dir,
            )
            if not steps:
                logger.error(
                    "skills_only orchestration requested for %s but no workflow skills were found (skills_dir=%s)",
                    workflow_id,
                    skills_dir or "<auto-discovery>",
                )
                return None
        else:
            manifest_steps = wf.steps or []
            if manifest_steps:
                for i, ms in enumerate(manifest_steps):
                    steps.append(WorkflowStep(
                        id=ms.get("id", f"step-{i+1}"),
                        description=ms.get("name", ms.get("description", f"Step {i+1}")),
                        engine=engine,
                        targets=ms.get("targets", []),
                        params=ms.get("params", {}),
                        outputs=ms.get("outputs", []),
                        depends_on=ms.get("depends_on", []),
                        max_retries=ms.get("max_retries", 0),
                        timeout=ms.get("timeout", 3600),
                        planning_source="workflow_manifest",
                        orchestration_reason=_workflow_step_reason(
                            planning_source="workflow_manifest",
                            description=ms.get("name", ms.get("description", f"Step {i+1}")),
                            depends_on=ms.get("depends_on", []),
                            outputs=ms.get("outputs", []),
                        ),
                    ))
            else:
                runner = SnakemakeRunner()
                targets = runner.list_targets(workflow_dir)
                if targets:
                    for i, target in enumerate(targets[:10]):
                        steps.append(WorkflowStep(
                            id=f"step-{i+1}",
                            description=f"Run Snakemake rule: {target}",
                            engine=engine,
                            targets=[target],
                            depends_on=[f"step-{i}"] if i > 0 else [],
                            planning_source="workflow_auto_discovery",
                            orchestration_reason=_workflow_step_reason(
                                planning_source="workflow_auto_discovery",
                                description=f"Run Snakemake rule: {target}",
                                depends_on=[f"step-{i}"] if i > 0 else [],
                                outputs=[],
                            ),
                        ))
                else:
                    steps.append(WorkflowStep(
                        id="step-1",
                        description="Run Snakemake workflow",
                        engine=engine,
                        planning_source="workflow_auto_discovery",
                        orchestration_reason=_workflow_step_reason(
                            planning_source="workflow_auto_discovery",
                            description="Run Snakemake workflow",
                            depends_on=[],
                            outputs=[],
                        ),
                    ))
    elif engine_str == "nextflow":
        runner = NextflowRunner()
        entries = runner.list_targets(workflow_dir)
        entry = entries[0] if entries else "main.nf"
        steps.append(WorkflowStep(
            id="step-1",
            description=f"Run Nextflow pipeline: {entry}",
            engine=WorkflowEngine.NEXTFLOW,
            entry=entry,
            params={"profile": "docker,test"},
            max_retries=0,
            planning_source="workflow_auto_discovery",
            orchestration_reason=_workflow_step_reason(
                planning_source="workflow_auto_discovery",
                description=f"Run Nextflow pipeline: {entry}",
                depends_on=[],
                outputs=[],
            ),
        ))
    else:
        # Fallback for R or other engines: create steps from manifest
        manifest_steps = wf.steps or []
        for i, ms in enumerate(manifest_steps):
            steps.append(WorkflowStep(
                id=ms.get("id", f"step-{i+1}"),
                description=ms.get("name", f"Step {i+1}"),
                engine=WorkflowEngine.PYTHON,
                entry=ms.get("script"),
                depends_on=ms.get("depends_on", []),
                planning_source="workflow_manifest",
                orchestration_reason=_workflow_step_reason(
                    planning_source="workflow_manifest",
                    description=ms.get("name", f"Step {i+1}"),
                    depends_on=ms.get("depends_on", []),
                    outputs=[],
                ),
            ))
        if not steps:
            steps.append(WorkflowStep(
                id="step-1",
                description="Run workflow",
                engine=WorkflowEngine.PYTHON,
                planning_source="workflow_auto_discovery",
                orchestration_reason=_workflow_step_reason(
                    planning_source="workflow_auto_discovery",
                    description="Run workflow",
                    depends_on=[],
                    outputs=[],
                ),
            ))

    _populate_implicit_input_refs(steps)

    return WorkflowPlan(
        id=run_id,
        workflow_id=workflow_id,
        workflow_dir=str(workflow_dir),
        work_dir=str(work_dir),
        steps=steps,
        status="queued",
    )


# ── LLM-powered planning ─────────────────────────────────────────────

def _generate_plan_via_llm(
    goal: str,
    data_profile: Dict,
    know_how: str = "",
    dataset_context: str = "",
    catalog_summary: str = "",
) -> Tuple[Optional[List[Dict]], Dict[str, Any]]:
    """Call the LLM to generate a JSON analysis plan."""
    prompt_messages: List[Any] = []
    llm = None
    try:
        llm = get_llm(temperature=0)

        # Build system prompt with optional know-how
        system_prompt = _PLAN_SYSTEM_PROMPT
        if know_how:
            system_prompt += f"\n\nDOMAIN KNOWLEDGE:\n{know_how[:4000]}\n"

        # Build the user message with context
        profile_summary = ""
        if data_profile:
            profile_summary = (
                f"\n\nData profile:\n"
                f"- File: {data_profile.get('file_path', 'unknown')}\n"
                f"- Rows: {data_profile.get('rows', '?')}\n"
                f"- Columns: {data_profile.get('columns', '?')}\n"
                f"- Column types: {json.dumps(data_profile.get('dtypes', {}), default=str)}\n"
                f"- Missing values: {json.dumps(data_profile.get('missing', {}), default=str)}\n"
            )
            # Include multi-file inventory if available
            all_files = data_profile.get("all_files", [])
            if all_files:
                profile_summary += f"- All available files ({len(all_files)}):\n"
                for af in all_files:
                    profile_summary += f"  - {af.get('filename', '?')} ({af.get('domain', 'unknown')}): {af['path']}\n"

        dataset_section = ""
        if catalog_summary:
            dataset_section = f"\n\n{catalog_summary}\n"
        elif dataset_context:
            dataset_section = f"\n\n{dataset_context}\n"

        user_msg = f"Goal: {goal}{profile_summary}{dataset_section}\n\nCreate an analysis plan."

        prompt_messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_msg),
        ]
        response = llm.invoke(prompt_messages)

        steps = parse_plan_json(response.content)
        trace_entry = build_llm_trace_entry(
            node="planner",
            purpose="create_plan",
            prompt_messages=prompt_messages,
            response=response,
            status="success" if steps else "parse_failed",
            parsed_output={
                "plan_step_count": len(steps or []),
                "step_ids": [step.get("id") for step in (steps or []) if isinstance(step, dict)],
            },
            context={"goal": goal[:500]},
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )
        if steps:
            logger.info("LLM generated plan with %d steps", len(steps))
            return steps, trace_entry
        else:
            logger.warning("Failed to parse LLM plan, falling back to default")
            return None, trace_entry

    except Exception as e:
        logger.error("LLM plan generation failed: %s", e)
        return None, build_llm_trace_entry(
            node="planner",
            purpose="create_plan",
            prompt_messages=prompt_messages,
            response=None,
            status="error",
            parsed_output=None,
            error=str(e),
            context={"goal": goal[:500]},
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )


def _replan_via_llm(
    goal: str,
    plan_steps: List[Dict],
    validation_result: Dict,
    qc_results: List[Dict],
) -> Tuple[Optional[List[Dict]], Dict[str, Any]]:
    """Call the LLM to revise the plan after a failure."""
    prompt_messages: List[Any] = []
    llm = None
    try:
        llm = get_llm(temperature=0.2)

        context = (
            f"Goal: {goal}\n\n"
            f"Current plan:\n{json.dumps(plan_steps, indent=2, default=str)}\n\n"
            f"Validation result:\n{json.dumps(validation_result, indent=2, default=str)}\n\n"
            f"QC results:\n{json.dumps(qc_results[-3:] if qc_results else [], indent=2, default=str)}\n\n"
            f"Revise the plan to address the failures."
        )

        prompt_messages = [
            SystemMessage(content=_REPLAN_SYSTEM_PROMPT),
            HumanMessage(content=context),
        ]
        response = llm.invoke(prompt_messages)

        steps = parse_plan_json(response.content)
        trace_entry = build_llm_trace_entry(
            node="planner",
            purpose="replan",
            prompt_messages=prompt_messages,
            response=response,
            status="success" if steps else "parse_failed",
            parsed_output={
                "plan_step_count": len(steps or []),
                "step_ids": [step.get("id") for step in (steps or []) if isinstance(step, dict)],
            },
            context={
                "goal": goal[:500],
                "validation_status": validation_result.get("status"),
            },
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )
        if steps:
            logger.info("LLM revised plan to %d steps", len(steps))
            return steps, trace_entry
        return None, trace_entry

    except Exception as e:
        logger.error("LLM replan failed: %s", e)
        return None, build_llm_trace_entry(
            node="planner",
            purpose="replan",
            prompt_messages=prompt_messages,
            response=None,
            status="error",
            parsed_output=None,
            error=str(e),
            context={
                "goal": goal[:500],
                "validation_status": validation_result.get("status"),
            },
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )


# ── Main planner node ─────────────────────────────────────────────────

def _check_hitl_steps(plan_steps: List[Dict]) -> Optional[Dict]:
    """Check if any pending step in the plan is a HITL step (type='hitl')."""
    for step in plan_steps:
        if step.get("type") == "hitl" and step.get("status", "pending") == "pending":
            return step
    return None


def _shorten_goal_for_hitl(goal: str) -> str:
    """Return a short, user-facing summary of the goal for HITL context. Strip dataset manifest."""
    if not goal:
        return "Current analysis"
    text = goal.strip()
    # Remove the long "=== AVAILABLE DATASETS ===" ... "=== END DATASETS ===" block
    if "=== AVAILABLE DATASETS ===" in text:
        start = text.find("=== AVAILABLE DATASETS ===")
        end = text.find("=== END DATASETS ===")
        if end != -1:
            end += len("=== END DATASETS ===")
            text = (text[:start] + text[end:]).strip()
        else:
            text = text[:start].strip()
    # Prefer first line (user request) and cap length
    first_line = text.split("\n")[0].strip() if text else ""
    if first_line and len(first_line) <= 280:
        return first_line
    if first_line:
        return first_line[:277] + "..."
    return text[:280] + "..." if len(text) > 280 else text


def _last_user_message_text(state: AgentState) -> str:
    msgs = state.get("messages", [])
    if not msgs:
        return ""
    return (getattr(msgs[-1], "content", "") or "").strip()


def _is_continue_message(content: str) -> bool:
    c = content.lower()
    keywords = [
        "continue", "proceed", "go ahead", "next step", "keep going",
        "yes", "go on", "carry on",
    ]
    return any(kw in c for kw in keywords)


def _is_correction_message(content: str) -> bool:
    c = content.lower()
    correction_keywords = [
        "correct path", "actual path", "right path", "the path is",
        "use this path", "here is the path", "try this",
        "the file is at", "located at", "found at",
    ]
    return any(kw in c for kw in correction_keywords)


def _is_answer_only_request(goal: str) -> bool:
    """True if the user wants a direct answer only (no code execution or data loading)."""
    if not goal:
        return False
    c = goal.lower()
    return any(
        phrase in c
        for phrase in (
            "general question",
            "just answer",
            "just answer me",
            "just give me a general answer",
            "just give me some general answer",
            "general answer",
            "answer me",
            "don't run",
            "dont run",
            "do not run",
            "no code",
            "don't execute",
            "dont execute",
            "no execution",
            "explain only",
            "answer without",
            "without running",
            "without executing",
        )
    )


def _has_strong_execution_intent(goal: str) -> bool:
    """True if the user clearly wants to run code / execute / load data (not just discuss)."""
    if not goal:
        return False
    c = goal.lower()
    return any(
        k in c
        for k in (
            "run the", "run my", "execute the", "execute my", "do the analysis", "perform the",
            "load the data", "load data", "profile the data", "profile data", "generate code",
            "run code", "run workflow", "execute workflow", "start the", "go ahead and run",
            "run it", "do it now", "run now", "execute now",
            "check the statistics", "check statistics", "do some analysis", "initial analysis",
            "run analysis", "compute stats", "get statistics", "analyze the data", "analyze data",
            "inventory", "missingness", "list all", "list the",
        )
    )


def _has_linked_context(state: AgentState) -> bool:
    """True if the session has linked dataset(s) or workflow (can run real analysis)."""
    if state.get("dataset_context") and str(state.get("dataset_context", "")).strip():
        return True
    if state.get("workflow_id_requested") or state.get("workflow_plan"):
        return True
    return False


def _goal_asks_for_data(goal: str) -> bool:
    """True if the goal clearly asks for data-related work (stats, profile, analysis, inventory)."""
    if not goal:
        return False
    c = goal.lower()
    return any(
        k in c
        for k in (
            "statistics", "stats", "profile", "analysis", "analyze", "inventory",
            "missingness", "check the data", "check data", "list all", "list the",
            "nrows", "ncols", "row count", "column count",
        )
    )


def _hitl_response_wants_general_answer(hitl_response: str) -> bool:
    """True if the user's HITL reply means 'skip details, just give a general answer' (no plan execution)."""
    if not hitl_response or not isinstance(hitl_response, str):
        return False
    c = hitl_response.strip().lower()
    if not c:
        return False
    return any(
        phrase in c
        for phrase in (
            "just give me a general answer",
            "just give me some general answer",
            "just give me general answer",
            "general answer",
            "just answer",
            "i dont know",
            "i don't know",
            "dont know",
            "don't know",
            "no preference",
            "any",
            "whatever",
            "skip",
            "just explain",
        )
    )


def planner_node(state: AgentState) -> Dict:
    """Central planner — decides the next action for the agent.

    Now supports Human-in-the-Loop (HITL):
    - If the LLM plan includes a step with type='hitl', route to HITL node
    - If a HITL response was just received, incorporate it and continue
    - If the user asks for a general answer only (no code), route straight to responder.
    """
    goal = state.get("goal") or "Analyze uploaded data"
    llm_trace = list(state.get("llm_trace") or [])
    orchestration_trace = list(state.get("orchestration_trace") or [])

    # ── 0a. Answer-only: user wants a direct reply, no execution ──────
    if _is_answer_only_request(goal):
        logger.info("Planner: answer-only request, routing to responder without execution")
        return {
            "next_node": "responder",
            "plan_steps": [],
            "plan_status": "completed",
            "current_step_id": "",
            "answer_only_goal": goal,
        }
    # When user selected "Ask" mode and the goal does not show strong execution intent, answer only (no plan/code).
    # Exception: if we have linked context and the goal asks for data (stats, profile, analysis), run a real plan.
    linked_and_data_request = _has_linked_context(state) and _goal_asks_for_data(goal)
    if "[Mode: ask]" in goal and not _has_strong_execution_intent(goal) and not linked_and_data_request:
        logger.info("Planner: Mode=ask and no strong execution intent, routing to responder")
        return {
            "next_node": "responder",
            "plan_steps": [],
            "plan_status": "completed",
            "current_step_id": "",
            "answer_only_goal": goal,
        }

    # When user selected "Ask" mode but the goal has strong execution intent (and no linked context), suggest mode switch.
    # When linked context + data request, we fall through to run a real plan below.
    if "[Mode: ask]" in goal and _has_strong_execution_intent(goal) and not linked_and_data_request:
        logger.info("Planner: Mode=ask but strong execution intent, suggesting mode switch to responder")
        return {
            "next_node": "responder",
            "plan_steps": [],
            "plan_status": "completed",
            "current_step_id": "",
            "answer_only_goal": goal,
            "suggested_mode": "analysis",
        }

    # ── 0. Check if we just received a HITL response ──────────────────
    hitl_response = state.get("hitl_response", "")
    hitl_clear: Dict = {}  # fields to clear if we had a HITL response
    if hitl_response:
        logger.info("Planner received HITL response: %s", hitl_response[:100])
        # If user said "just give me a general answer" / "I dont know" etc., skip plan and answer only
        if _hitl_response_wants_general_answer(hitl_response):
            logger.info("Planner: HITL response asks for general answer only, routing to responder")
            return {
                "hitl_pending": False,
                "hitl_response": "",
                "hitl_question": "",
                "hitl_context": "",
                "hitl_reason": "",
                "next_node": "responder",
                "plan_steps": [],
                "plan_status": "completed",
                "current_step_id": "",
                "answer_only_goal": f"{goal}\n\nUser said: {hitl_response}",
            }
        # Mark any pending HITL steps as completed so we don't loop
        plan_steps = list(state.get("plan_steps", []))
        for step in plan_steps:
            if step.get("type") == "hitl" and step.get("status", "pending") == "pending":
                step["status"] = "completed"
                step["result"] = hitl_response
        hitl_clear = {
            "hitl_pending": False,
            "hitl_response": "",
            "hitl_question": "",
            "hitl_context": "",
            "hitl_reason": "",
            "plan_steps": plan_steps,
        }
        # Incorporate the HITL answer into the goal context
        goal = f"{goal}\n\nUser clarification: {hitl_response}"
        # After HITL, find next executable step and proceed
        next_step = select_next_step(plan_steps)
        if next_step:
            orchestration_trace = append_trace(
                orchestration_trace,
                build_orchestration_trace_entry(
                    event_type="generic_step_selected",
                    step_id=str(next_step["id"]),
                    reason=(
                        f"Selected '{next_step['id']}' after incorporating HITL clarification. "
                        f"{next_step.get('orchestration_reason', '')}"
                    ).strip(),
                    details={"stage": "after_hitl"},
                ),
            )
            return {
                **hitl_clear,
                "goal": goal,
                "next_node": "coder",
                "plan_status": "executing",
                "current_step_id": next_step["id"],
                "orchestration_trace": orchestration_trace,
            }
        else:
            # All steps done (shouldn't happen right after HITL, but be safe)
            return {**hitl_clear, "next_node": "responder", "plan_status": "completed"}

    # ── 0b. Explicit workflow binding (experiment-linked workflows) ──
    explicit_wf_id = state.get("workflow_id_requested")
    if explicit_wf_id and not state.get("workflow_plan"):
        plan = _create_workflow_plan(explicit_wf_id, state)
        if not plan:
            return {
                "workflow_id_requested": explicit_wf_id,
                "workflow_status": "failed",
                "workflow_run_context": {
                    "run_id": "",
                    "workflow_id": explicit_wf_id,
                    "status": "failed",
                    "error_summary": f"Workflow '{explicit_wf_id}' not found or invalid.",
                    "ended_at": _now_iso(),
                },
                "next_node": "responder",
            }

        run_ctx = dict(state.get("workflow_run_context") or {})
        strict_manifest = bool(run_ctx.get("strict_manifest", True))
        orchestration_trace = append_trace(
            orchestration_trace,
            _workflow_plan_created_event(
                plan,
                mode=str(run_ctx.get("orchestration_mode") or "manifest_or_default"),
                skills_only=_skills_only_mode(run_ctx),
            ),
        )
        ready = plan.ready_steps(strict_manifest=strict_manifest)
        first_step = None
        selected_via_llm = False
        if ready:
            if str(run_ctx.get("step_selection") or "").strip().lower() == "llm":
                selected_id, llm_entry = _select_workflow_step_via_llm(
                    plan,
                    ready,
                    workflow_id=str(plan.workflow_id),
                )
                llm_trace = append_trace(llm_trace, llm_entry)
                if selected_id:
                    first_step = plan.get_step(selected_id)
                    selected_via_llm = True
                    orchestration_trace = append_trace(
                        orchestration_trace,
                        build_orchestration_trace_entry(
                            event_type="workflow_step_selected",
                            workflow_id=plan.workflow_id,
                            step_id=selected_id,
                            reason=f"Selected '{selected_id}' from the ready set using LLM step selection.",
                            details={
                                "strict_manifest": strict_manifest,
                                "ready_step_ids": [s.id for s in ready],
                                "stage": "workflow_start",
                            },
                        ),
                    )
            if first_step is None:
                first_step = plan.get_next_step(strict_manifest=strict_manifest)
        if first_step is None:
            return {
                "workflow_plan": plan.to_dict(),
                "plan_steps": plan.to_plan_steps(),
                "workflow_status": "failed",
                "orchestration_trace": orchestration_trace,
                "workflow_run_context": {
                    "run_id": plan.id,
                    "workflow_id": explicit_wf_id,
                    "status": "failed",
                    "error_summary": "Workflow has no executable steps.",
                    "ended_at": _now_iso(),
                },
                "llm_trace": llm_trace,
                "next_node": "responder",
            }

        if not selected_via_llm:
            orchestration_trace = append_trace(
                orchestration_trace,
                _workflow_step_selected_event(
                    plan,
                    first_step,
                    strict_manifest=strict_manifest,
                    stage="workflow_start",
                ),
            )
        if first_step.engine == WorkflowEngine.AGENT:
            first_step.status = StepStatus.RUNNING
            plan.current_step_id = first_step.id
            plan.status = "executing"

        workflow = get_workflow_by_id(explicit_wf_id)
        run_ctx.update({
            "run_id": plan.id,
            "workflow_id": explicit_wf_id,
            "engine": (workflow.engine if workflow else "agent"),
            "experiment_id": state.get("experiment_id"),
            "session_id": state.get("session_id"),
            "execution_mode": run_ctx.get("execution_mode", "interactive"),
            "strict_manifest": run_ctx.get("strict_manifest", True),
            "status": "running",
            "current_step_id": first_step.id,
            "started_at": run_ctx.get("started_at", _now_iso()),
            "ended_at": None,
            "error_summary": "",
        })
        result: Dict[str, Any] = {
            "workflow_plan": plan.to_dict(),
            "plan_steps": plan.to_plan_steps(),
            "workflow_id_requested": explicit_wf_id,
            "workflow_status": "running",
            "workflow_run_id": plan.id,
            "workflow_run_context": run_ctx,
            "execution_workdir": plan.work_dir,
            "plan_status": "executing",
            "current_step_id": first_step.id,
            "orchestration_trace": orchestration_trace,
            "llm_trace": llm_trace,
            "next_node": "coder" if first_step.engine == WorkflowEngine.AGENT else "executor",
        }
        if first_step.engine == WorkflowEngine.AGENT:
            base_goal = first_step.prompt_hint or first_step.description
            result["goal"] = _inject_error_book_lessons_into_goal(
                base_goal,
                error_book=state.get("error_book", []) or [],
                workflow_id=explicit_wf_id,
            )
        return result

    # ── 0c. Resume existing plan if user says "continue" ────────────
    existing_plan = state.get("plan_steps", [])
    if existing_plan and not state.get("workflow_plan"):
        last_msg = _last_user_message_text(state)
        is_continue = _is_continue_message(last_msg)
        is_correction = _is_correction_message(last_msg)

        next_pending = select_next_step(existing_plan)

        # If user says "continue" but no pending step exists, check if
        # there's a failed step we can reset and retry (e.g. after code
        # fix or error pattern update).
        if (is_continue or is_correction) and not next_pending:
            for step in existing_plan:
                if step.get("status") == "failed":
                    logger.info(
                        "Resetting failed step '%s' to pending for retry (user said continue)",
                        step.get("id"),
                    )
                    step["status"] = "pending"
                    next_pending = step
                    break
            # Also reset workflow_plan step status if applicable
            plan_data = state.get("workflow_plan")
            if plan_data and isinstance(plan_data, dict):
                wf_steps = plan_data.get("steps", [])
                for ws in wf_steps:
                    if ws.get("status") == "failed":
                        ws["status"] = "pending"
                        ws["retry_count"] = 0
                        break
                plan_data["status"] = "executing"

        if (is_continue or is_correction) and next_pending:
            # If the user provided new info (like a corrected path),
            # update the goal so the coder can see the correction.
            updated_goal = goal
            if is_correction and last_msg:
                updated_goal = f"{goal}\n\nUser correction: {last_msg}"
            logger.info("Resuming plan: next step = %s (correction=%s)",
                        next_pending["id"], is_correction)
            orchestration_trace = append_trace(
                orchestration_trace,
                build_orchestration_trace_entry(
                    event_type="generic_step_selected",
                    step_id=str(next_pending["id"]),
                    reason=(
                        f"Selected '{next_pending['id']}' while resuming the existing plan. "
                        f"continue={is_continue}, correction={is_correction}. "
                        f"{next_pending.get('orchestration_reason', '')}"
                    ).strip(),
                    details={
                        "stage": "plan_resume",
                        "plan_status": state.get("plan_status"),
                        "depends_on": next_pending.get("depends_on", []),
                    },
                ),
            )
            result = {
                "next_node": "coder",
                "plan_status": "executing",
                "current_step_id": next_pending["id"],
                "plan_steps": existing_plan,
                "orchestration_trace": orchestration_trace,
                "retry_count": 0,            # reset retry counter for fresh attempt
                "validation_result": {},     # clear previous failures
            }
            # Include reset workflow plan if we modified it
            plan_data = state.get("workflow_plan")
            if plan_data:
                result["workflow_plan"] = plan_data
            if updated_goal != goal:
                result["goal"] = updated_goal
            return result

    # ── 1. Active workflow plan handling ──────────────────────────────
    plan_data = state.get("workflow_plan")
    if plan_data:
        plan = WorkflowPlan.from_dict(plan_data)
        run_ctx = dict(state.get("workflow_run_context") or {})
        execution_mode = run_ctx.get("execution_mode", "interactive")
        strict_manifest = bool(run_ctx.get("strict_manifest", True))
        last_msg = _last_user_message_text(state)
        is_continue = _is_continue_message(last_msg)
        is_correction = _is_correction_message(last_msg)

        if execution_mode == "interactive" and state.get("workflow_status") == "waiting_user":
            if not (is_continue or is_correction):
                run_ctx["status"] = "waiting_user"
                return {
                    "workflow_status": "waiting_user",
                    "workflow_run_context": run_ctx,
                    "validation_result": {
                        "status": "waiting",
                        "detail": "Reply 'continue' to run the next workflow step.",
                    },
                    "next_node": "responder",
                }
            run_ctx["status"] = "running"

        # Allow conversational retry for workflow failures:
        # if user says "continue" (or provides a correction) and there is no
        # pending step, reset the first failed step back to pending.
        if is_continue or is_correction:
            has_pending = any(s.status == StepStatus.PENDING for s in plan.steps)
            if not has_pending:
                for s in plan.steps:
                    if s.status == StepStatus.FAILED:
                        logger.info(
                            "Resetting failed workflow step '%s' to pending for retry (continue/correction).",
                            s.id,
                        )
                        s.status = StepStatus.PENDING
                        s.error = None
                        # User explicitly asked to rerun, so start a fresh retry window.
                        s.retry_count = 0
                        plan.status = "executing"
                        run_ctx["status"] = "running"
                        run_ctx["ended_at"] = None
                        break

        if plan.is_complete():
            plan.status = "completed"
            run_ctx.update({
                "status": "success",
                "current_step_id": plan.current_step_id,
                "ended_at": _now_iso(),
            })
            orchestration_trace = append_trace(
                orchestration_trace,
                build_orchestration_trace_entry(
                    event_type="workflow_completed",
                    workflow_id=plan.workflow_id,
                    step_id=plan.current_step_id or "",
                    reason="All workflow steps are complete.",
                    details={"plan_id": plan.id},
                ),
            )
            return {
                "workflow_plan": plan.to_dict(),
                "plan_steps": plan.to_plan_steps(),
                "next_node": "responder",
                "plan_status": "completed",
                "workflow_status": "success",
                "workflow_run_context": run_ctx,
                "orchestration_trace": orchestration_trace,
            }
        any_failed = any(s.status == StepStatus.FAILED for s in plan.steps)
        # Only declare the whole workflow as failed if there are truly no
        # pending/retryable steps left.  The "continue" handler in section 0b
        # may have reset a failed step to PENDING already, so re-check.
        has_pending = any(s.status == StepStatus.PENDING for s in plan.steps)
        if (plan.has_failed() or any_failed) and not has_pending:
            plan.status = "failed"
            run_ctx.update({
                "status": "failed",
                "current_step_id": plan.current_step_id,
                "ended_at": _now_iso(),
            })
            failed_step = next((s for s in plan.steps if s.status == StepStatus.FAILED), None)
            orchestration_trace = append_trace(
                orchestration_trace,
                build_orchestration_trace_entry(
                    event_type="workflow_failed",
                    workflow_id=plan.workflow_id,
                    step_id=(failed_step.id if failed_step else plan.current_step_id or ""),
                    reason=(
                        f"Workflow stopped because there are failed steps with no pending alternatives. "
                        f"failed_step={(failed_step.id if failed_step else plan.current_step_id or '')}."
                    ),
                    details={"plan_id": plan.id},
                ),
            )
            return {
                "workflow_plan": plan.to_dict(),
                "plan_steps": plan.to_plan_steps(),
                "next_node": "responder",
                "plan_status": "failed",
                "workflow_status": "failed",
                "workflow_run_context": run_ctx,
                "orchestration_trace": orchestration_trace,
            }
        ready = plan.ready_steps(strict_manifest=strict_manifest)
        next_step = None
        selected_via_llm = False
        if ready:
            if str(run_ctx.get("step_selection") or "").strip().lower() == "llm":
                selected_id, llm_entry = _select_workflow_step_via_llm(
                    plan,
                    ready,
                    workflow_id=str(plan.workflow_id),
                )
                llm_trace = append_trace(llm_trace, llm_entry)
                if selected_id:
                    next_step = plan.get_step(selected_id)
                    selected_via_llm = True
                    orchestration_trace = append_trace(
                        orchestration_trace,
                        build_orchestration_trace_entry(
                            event_type="workflow_step_selected",
                            workflow_id=plan.workflow_id,
                            step_id=selected_id,
                            reason=f"Selected '{selected_id}' from the ready set using LLM step selection.",
                            details={
                                "strict_manifest": strict_manifest,
                                "ready_step_ids": [s.id for s in ready],
                            },
                        ),
                    )
            if next_step is None:
                next_step = plan.get_next_step(strict_manifest=strict_manifest)
        if next_step:
            if not selected_via_llm:
                orchestration_trace = append_trace(
                    orchestration_trace,
                    _workflow_step_selected_event(
                        plan,
                        next_step,
                        strict_manifest=strict_manifest,
                        stage="workflow_resume",
                    ),
                )
            # For agent-driven workflow steps, route through the LLM plan
            if next_step.engine == WorkflowEngine.AGENT:
                mode = next_step.mode or StepMode.AGENT_CODE.value
                # Build a contextual goal from prompt_hint
                step_goal = next_step.prompt_hint or next_step.description
                step_goal = _inject_error_book_lessons_into_goal(
                    step_goal,
                    error_book=state.get("error_book", []) or [],
                    workflow_id=plan.workflow_id,
                )
                know_how = state.get("know_how_context", "")
                ds_ctx = state.get("dataset_context", "")

                if strict_manifest:
                    next_step.status = StepStatus.RUNNING
                    plan.current_step_id = next_step.id
                    run_ctx.update({"status": "running", "current_step_id": next_step.id})
                    return {
                        "workflow_plan": plan.to_dict(),
                        "plan_steps": plan.to_plan_steps(),
                        "workflow_status": "running",
                        "workflow_run_context": run_ctx,
                        "orchestration_trace": orchestration_trace,
                        "llm_trace": llm_trace,
                        "goal": step_goal,
                        "next_node": "coder",
                        "plan_status": "executing",
                        "current_step_id": next_step.id,
                    }

                if mode in (StepMode.AGENT_GENERATE.value, StepMode.AGENT_VALIDATE.value):
                    # These are LLM-reasoning steps: create an LLM plan for this step
                    cat_summary = build_catalog_summary(state.get("data_catalog", []))
                    llm_steps, llm_entry = _generate_plan_via_llm(step_goal, state.get("data_profile", {}), know_how, dataset_context=ds_ctx, catalog_summary=cat_summary)
                    llm_trace = append_trace(llm_trace, llm_entry)
                    if llm_steps:
                        llm_steps = _annotate_generic_plan_steps(llm_steps, planning_source="planner_llm")
                        plan_result = init_plan(step_goal, llm_steps)
                        orchestration_trace = append_trace(
                            orchestration_trace,
                            _generic_plan_created_event(
                                goal=step_goal,
                                planning_source="planner_llm",
                                plan_steps=plan_result.get("plan_steps", []),
                            ),
                        )
                        # Check if this step requires HITL after completion
                        if next_step.hitl == "review_required":
                            # Add a HITL step at the end of the generated plan
                            plan_result["plan_steps"].append({
                                "id": f"hitl-{next_step.id}",
                                "type": "hitl",
                                "title": f"Review: {next_step.description}",
                                "description": f"Please review the output of '{next_step.description}' before proceeding.",
                                "status": "pending",
                            })
                        next_step.status = StepStatus.RUNNING
                        plan.current_step_id = next_step.id
                        run_ctx.update({"status": "running", "current_step_id": next_step.id})
                        return {
                            **plan_result,
                            "workflow_plan": plan.to_dict(),
                            "workflow_status": "running",
                            "workflow_run_context": run_ctx,
                            "llm_trace": llm_trace,
                            "orchestration_trace": orchestration_trace,
                            "goal": step_goal,
                            "next_node": "coder",
                            "plan_status": "executing",
                        }
                    # Fallback: route to coder directly
                    next_step.status = StepStatus.RUNNING
                    plan.current_step_id = next_step.id
                    run_ctx.update({"status": "running", "current_step_id": next_step.id})
                    return {
                        "workflow_plan": plan.to_dict(),
                        "plan_steps": plan.to_plan_steps(),
                        "workflow_status": "running",
                        "workflow_run_context": run_ctx,
                        "llm_trace": llm_trace,
                        "orchestration_trace": orchestration_trace,
                        "goal": step_goal,
                        "next_node": "coder",
                        "plan_status": "executing",
                        "current_step_id": next_step.id,
                    }
                else:
                    # agent_code mode: route to coder
                    next_step.status = StepStatus.RUNNING
                    plan.current_step_id = next_step.id
                    run_ctx.update({"status": "running", "current_step_id": next_step.id})
                    return {
                        "workflow_plan": plan.to_dict(),
                        "plan_steps": plan.to_plan_steps(),
                        "workflow_status": "running",
                        "workflow_run_context": run_ctx,
                        "orchestration_trace": orchestration_trace,
                        "llm_trace": llm_trace,
                        "goal": step_goal,
                        "next_node": "coder",
                        "plan_status": "executing",
                        "current_step_id": next_step.id,
                    }
            else:
                # Non-agent steps (snakemake, nextflow, python): route to executor
                plan.current_step_id = next_step.id
                run_ctx.update({"status": "running", "current_step_id": next_step.id})
                return {
                    "workflow_plan": plan.to_dict(),
                    "plan_steps": plan.to_plan_steps(),
                    "workflow_status": "running",
                    "workflow_run_context": run_ctx,
                    "orchestration_trace": orchestration_trace,
                    "llm_trace": llm_trace,
                    "current_step_id": next_step.id,
                    "next_node": "executor",
                    "plan_status": "executing",
                }

    # ── 2. Workflow intent detection ──────────────────────────────────
    workflow_id = _detect_workflow_intent(state)
    if workflow_id:
        plan = _create_workflow_plan(workflow_id, state)
        if plan:
            strict_manifest = bool((state.get("workflow_run_context") or {}).get("strict_manifest", True))
            run_ctx = dict(state.get("workflow_run_context") or {})
            orchestration_trace = append_trace(
                orchestration_trace,
                _workflow_plan_created_event(
                    plan,
                    mode=str(run_ctx.get("orchestration_mode") or "intent_detected"),
                    skills_only=_skills_only_mode(run_ctx),
                ),
            )
            first_step = plan.get_next_step(strict_manifest=strict_manifest)
            if not first_step:
                return {
                    "workflow_id_requested": workflow_id,
                    "workflow_status": "failed",
                    "orchestration_trace": orchestration_trace,
                    "workflow_run_context": {
                        "run_id": plan.id,
                        "workflow_id": workflow_id,
                        "status": "failed",
                        "error_summary": "Workflow has no executable steps.",
                        "ended_at": _now_iso(),
                    },
                    "next_node": "responder",
                }

            orchestration_trace = append_trace(
                orchestration_trace,
                _workflow_step_selected_event(
                    plan,
                    first_step,
                    strict_manifest=strict_manifest,
                    stage="workflow_intent_start",
                ),
            )
            if first_step.engine == WorkflowEngine.AGENT:
                first_step.status = StepStatus.RUNNING
                plan.current_step_id = first_step.id
                plan.status = "executing"

            wf = get_workflow_by_id(workflow_id)
            run_ctx.update({
                "run_id": plan.id,
                "workflow_id": workflow_id,
                "engine": (wf.engine if wf else "agent"),
                "experiment_id": state.get("experiment_id"),
                "session_id": state.get("session_id"),
                "execution_mode": run_ctx.get("execution_mode", "interactive"),
                "strict_manifest": run_ctx.get("strict_manifest", True),
                "status": "running",
                "current_step_id": first_step.id,
                "started_at": run_ctx.get("started_at", _now_iso()),
                "ended_at": None,
                "error_summary": "",
            })
            payload: Dict[str, Any] = {
                "workflow_plan": plan.to_dict(),
                "plan_steps": plan.to_plan_steps(),
                "workflow_id_requested": workflow_id,
                "workflow_status": "running",
                "workflow_run_id": plan.id,
                "workflow_run_context": run_ctx,
                "execution_workdir": plan.work_dir,
                "next_node": "coder" if first_step.engine == WorkflowEngine.AGENT else "executor",
                "plan_status": "executing",
                "current_step_id": first_step.id,
                "orchestration_trace": orchestration_trace,
            }
            if first_step.engine == WorkflowEngine.AGENT:
                base_goal = first_step.prompt_hint or first_step.description
                payload["goal"] = _inject_error_book_lessons_into_goal(
                    base_goal,
                    error_book=state.get("error_book", []) or [],
                    workflow_id=workflow_id,
                )
            return payload
        return {
            "workflow_id_requested": workflow_id,
            "workflow_status": "failed",
            "next_node": "responder",
        }

    # ── 3. Check if QC/validation failed and we need to replan ────────
    validation = state.get("validation_result", {})
    qc_results = state.get("qc_results", [])
    if validation.get("status") == "fail" or (qc_results and qc_results[-1].get("status") == "fail"):
        revised_steps, llm_entry = _replan_via_llm(
            goal,
            state.get("plan_steps", []),
            validation,
            qc_results,
        )
        llm_trace = append_trace(llm_trace, llm_entry)
        if revised_steps:
            revised_steps = _annotate_generic_plan_steps(revised_steps, planning_source="planner_replan_llm")
            plan_data = init_plan(goal, revised_steps)
            plan_data["plan_version"] = state.get("plan_version", 1) + 1
            orchestration_trace = append_trace(
                orchestration_trace,
                _generic_plan_created_event(
                    goal=goal,
                    planning_source="planner_replan_llm",
                    plan_steps=plan_data.get("plan_steps", []),
                ),
            )
            return {
                **plan_data,
                "llm_trace": llm_trace,
                "orchestration_trace": orchestration_trace,
                "next_node": "coder",
                "validation_result": {},   # reset
            }

    # ── 4. Create initial plan via LLM if none exists ─────────────────
    if not state.get("plan_steps"):
        data_profile = state.get("data_profile", {})
        know_how = state.get("know_how_context", "")
        ds_ctx = state.get("dataset_context", "")
        cat_summary = build_catalog_summary(state.get("data_catalog", []))
        llm_steps, llm_entry = _generate_plan_via_llm(goal, data_profile, know_how=know_how, dataset_context=ds_ctx, catalog_summary=cat_summary)
        llm_trace = append_trace(llm_trace, llm_entry)
        if llm_steps:
            llm_steps = _annotate_generic_plan_steps(llm_steps, planning_source="planner_llm")
        plan_data = init_plan(goal, llm_steps)  # llm_steps can be None -> fallback
        planning_source = "planner_llm" if llm_steps else "planner_fallback"
        if not llm_steps:
            plan_data["plan_steps"] = _annotate_generic_plan_steps(
                plan_data.get("plan_steps", []),
                planning_source=planning_source,
            )
        orchestration_trace = append_trace(
            orchestration_trace,
            _generic_plan_created_event(
                goal=goal,
                planning_source=planning_source,
                plan_steps=plan_data.get("plan_steps", []),
            ),
        )

        # Plan mode: build plan only, then return to responder (no coder/executor).
        if "[Mode: plan]" in goal:
            logger.info("Planner: Mode=plan, returning plan to responder without execution")
            return {
                **plan_data,
                "llm_trace": llm_trace,
                "orchestration_trace": orchestration_trace,
                "next_node": "responder",
                "plan_status": "planned",
            }

        # Check if the plan contains any HITL steps that need human input
        hitl_step = _check_hitl_steps(plan_data.get("plan_steps", []))
        if hitl_step:
            short_goal = _shorten_goal_for_hitl(goal)
            return {
                **plan_data,
                "llm_trace": llm_trace,
                "orchestration_trace": orchestration_trace,
                "hitl_pending": True,
                "hitl_question": hitl_step.get("question", hitl_step.get("description", "")),
                "hitl_context": short_goal,
                "hitl_reason": "The analysis plan requires clarification before proceeding.",
                "hitl_origin_node": "planner",
                "next_node": "hitl",
            }

        # Route to data_ingest if we have no data profile AND haven't
        # tried data_ingest yet (the flag prevents infinite loops).
        should_ingest = (
            not data_profile
            and not state.get("_data_ingest_attempted")
        )
        # After data_ingest completes, route to data_analyst(init) to build
        # the full catalog before the coder runs.
        needs_catalog = (
            data_profile
            and not state.get("data_catalog")
        )
        # Select the first pending step so coder knows what to generate for
        first_step = select_next_step(plan_data.get("plan_steps", []))
        first_step_id = first_step["id"] if first_step else None

        if should_ingest:
            next_dest = "data_ingest"
        elif needs_catalog:
            next_dest = "data_analyst"
            plan_data["data_analyst_mode"] = "init"
        else:
            next_dest = "coder"

        return {
            **plan_data,
            "llm_trace": llm_trace,
            "orchestration_trace": orchestration_trace,
            "current_step_id": first_step_id,
            "next_node": next_dest,
        }

    # ── 5. Check for HITL steps in existing plan ──────────────────────
    hitl_step = _check_hitl_steps(state.get("plan_steps", []))
    if hitl_step:
        short_goal = _shorten_goal_for_hitl(goal)
        return {
            "hitl_pending": True,
            "hitl_question": hitl_step.get("question", hitl_step.get("description", "")),
            "hitl_context": short_goal,
            "hitl_reason": "A plan step requires human input before proceeding.",
            "hitl_origin_node": "planner",
            "current_step_id": hitl_step["id"],
            "next_node": "hitl",
        }

    # ── 6. Drive the existing plan forward ────────────────────────────
    next_step = select_next_step(state.get("plan_steps", []))
    if not next_step:
        return {
            "next_node": "responder",
            "plan_status": "completed",
            "llm_trace": llm_trace,
        }

    orchestration_trace = append_trace(
        orchestration_trace,
        build_orchestration_trace_entry(
            event_type="generic_step_selected",
            step_id=str(next_step["id"]),
            reason=(
                f"Selected '{next_step['id']}' as the next generic plan step. "
                f"{next_step.get('orchestration_reason', '')}"
            ).strip(),
            details={
                "stage": "generic_plan_progress",
                "depends_on": next_step.get("depends_on", []),
                "required_node": next_step.get("required_node"),
            },
        ),
    )

    # Determine what this step needs — route to data_ingest if no profile
    # and either the step is data_prep or we have an experiment with datasets.
    needs_ingest = (
        not state.get("data_profile")
        and not state.get("_data_ingest_attempted")
        and (next_step.get("type") == "data_prep" or state.get("experiment_id"))
    )
    if needs_ingest:
        return {
            "next_node": "data_ingest",
            "plan_status": "executing",
            "current_step_id": next_step["id"],
            "llm_trace": llm_trace,
            "orchestration_trace": orchestration_trace,
        }
    # Route to data_analyst if profile exists but catalog is empty
    if state.get("data_profile") and not state.get("data_catalog"):
        return {
            "next_node": "data_analyst",
            "data_analyst_mode": "init",
            "plan_status": "executing",
            "current_step_id": next_step["id"],
            "llm_trace": llm_trace,
            "orchestration_trace": orchestration_trace,
        }
    if not state.get("data_profile") and next_step.get("type") == "data_prep":
        # data_ingest already tried, skip to coder (which can load data inline)
        return {
            "next_node": "coder",
            "plan_status": "executing",
            "current_step_id": next_step["id"],
            "llm_trace": llm_trace,
            "orchestration_trace": orchestration_trace,
        }

    if not state.get("code_scratchpad"):
        return {
            "next_node": "coder",
            "plan_status": "executing",
            "current_step_id": next_step["id"],
            "llm_trace": llm_trace,
            "orchestration_trace": orchestration_trace,
        }

    return {
        "next_node": "executor",
        "plan_status": "executing",
        "current_step_id": next_step["id"],
        "llm_trace": llm_trace,
        "orchestration_trace": orchestration_trace,
    }
