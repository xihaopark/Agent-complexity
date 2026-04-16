"""Workflow step model for stepwise execution."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class StepStatus(str, Enum):
    """Status of a workflow step."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowEngine(str, Enum):
    """Supported workflow engines."""
    SNAKEMAKE = "snakemake"
    NEXTFLOW = "nextflow"
    PYTHON = "python"  # For code execution
    AGENT = "agent"  # AI agent-driven (no pre-written scripts)


class StepMode(str, Enum):
    """Execution mode for agent-driven workflow steps."""
    AGENT_GENERATE = "agent_generate"  # Agent produces a document/spec from scratch
    AGENT_VALIDATE = "agent_validate"  # Agent reviews/validates previous step output
    AGENT_CODE = "agent_code"          # Agent writes and executes code
    EXECUTE_SCRIPT = "execute_script"  # Run a pre-written script (v1 behavior)


@dataclass
class WorkflowStep:
    """A single step in a workflow execution plan.
    
    Steps are the atomic units of execution that the state machine manages.
    The Planner creates steps; the Executor runs them via Runners.
    """
    id: str
    description: str
    engine: WorkflowEngine
    status: StepStatus = StepStatus.PENDING
    
    # Execution targets
    targets: List[str] = field(default_factory=list)  # For Snakemake rules
    entry: Optional[str] = None  # For Nextflow entry point
    code: Optional[str] = None  # For Python code
    
    # Agent-driven step fields
    mode: Optional[str] = None  # StepMode value for agent workflows
    prompt_hint: Optional[str] = None  # Guidance for the LLM planner
    hitl: Optional[str] = None  # "review_required", "optional", "on_failure", or None
    input_refs: List[str] = field(default_factory=list)  # Relative paths to input data
    output_type: Optional[str] = None  # "document", "dataset", "report", etc.
    
    # Inputs and outputs
    inputs: Dict[str, str] = field(default_factory=dict)  # name -> path
    outputs: List[str] = field(default_factory=list)  # expected output paths
    artifacts: List[str] = field(default_factory=list)  # actual output paths
    
    # Execution metadata
    params: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)  # step ids
    retry_count: int = 0
    max_retries: int = 2
    timeout: int = 3600  # seconds
    planning_source: Optional[str] = None
    orchestration_reason: Optional[str] = None

    # Results
    stdout: str = ""
    stderr: str = ""
    error: Optional[str] = None

    def _normalize_ref(self, ref: str) -> str:
        return str(ref or "").strip().replace("\\", "/").lstrip("./")

    def _matches_available_ref(self, ref: str, available_refs: set[str]) -> bool:
        normalized = self._normalize_ref(ref)
        if not normalized:
            return False
        if normalized in available_refs:
            return True
        for candidate in available_refs:
            if candidate.endswith(f"/{normalized}") or normalized.endswith(f"/{candidate}"):
                return True
        return False

    def inputs_ready(self, available_refs: set[str]) -> bool:
        if not self.input_refs:
            return True
        return all(self._matches_available_ref(ref, available_refs) for ref in self.input_refs)

    def can_run(
        self,
        completed_steps: List[str],
        available_refs: Optional[set[str]] = None,
        strict_manifest: bool = True,
    ) -> bool:
        """Check if this step can run."""
        if self.status != StepStatus.PENDING:
            return False
        deps_ready = all(dep in completed_steps for dep in self.depends_on)
        if strict_manifest:
            return deps_ready
        if self.depends_on and not deps_ready:
            return False
        if self.input_refs:
            return self.inputs_ready(available_refs or set())
        if self.depends_on:
            return deps_ready
        return True

    def can_retry(self) -> bool:
        """Check if this step can be retried."""
        return self.status == StepStatus.FAILED and self.retry_count < self.max_retries

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state serialization."""
        return {
            "id": self.id,
            "description": self.description,
            "engine": self.engine.value,
            "status": self.status.value,
            "targets": self.targets,
            "entry": self.entry,
            "code": self.code,
            "mode": self.mode,
            "prompt_hint": self.prompt_hint,
            "hitl": self.hitl,
            "input_refs": self.input_refs,
            "output_type": self.output_type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "artifacts": self.artifacts,
            "params": self.params,
            "depends_on": self.depends_on,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "planning_source": self.planning_source,
            "orchestration_reason": self.orchestration_reason,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowStep":
        """Create from dictionary."""
        engine_val = data.get("engine", "python")
        try:
            engine = WorkflowEngine(engine_val)
        except ValueError:
            engine = WorkflowEngine.PYTHON
        return cls(
            id=data["id"],
            description=data.get("description", ""),
            engine=engine,
            status=StepStatus(data.get("status", "pending")),
            targets=data.get("targets", []),
            entry=data.get("entry"),
            code=data.get("code"),
            mode=data.get("mode"),
            prompt_hint=data.get("prompt_hint"),
            hitl=data.get("hitl"),
            input_refs=data.get("input_refs", []),
            output_type=data.get("output_type"),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", []),
            artifacts=data.get("artifacts", []),
            params=data.get("params", {}),
            depends_on=data.get("depends_on", []),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 2),
            timeout=data.get("timeout", 3600),
            planning_source=data.get("planning_source"),
            orchestration_reason=data.get("orchestration_reason"),
            stdout=data.get("stdout", ""),
            stderr=data.get("stderr", ""),
            error=data.get("error"),
        )


@dataclass
class WorkflowPlan:
    """A plan consisting of multiple workflow steps.
    
    The Planner creates and manages the plan; Executor runs steps one by one.
    """
    id: str
    workflow_id: str
    workflow_dir: str
    work_dir: str
    steps: List[WorkflowStep] = field(default_factory=list)
    current_step_id: Optional[str] = None
    status: str = "draft"  # draft / executing / completed / failed

    def completed_step_ids(self) -> List[str]:
        return [s.id for s in self.steps if s.status == StepStatus.SUCCESS]

    def available_refs(self) -> set[str]:
        refs: set[str] = set()
        for step in self.steps:
            if step.status != StepStatus.SUCCESS:
                continue
            refs.add(step.id)
            refs.update(
                step._normalize_ref(ref)
                for ref in [*step.outputs, *step.artifacts]
                if step._normalize_ref(ref)
            )
        return refs

    def ready_steps(self, strict_manifest: bool = True) -> List[WorkflowStep]:
        completed = self.completed_step_ids()
        available_refs = self.available_refs()
        return [
            step
            for step in self.steps
            if step.can_run(
                completed,
                available_refs=available_refs,
                strict_manifest=strict_manifest,
            )
        ]

    def _downstream_unlock_score(self, step_id: str) -> int:
        seen: set[str] = set()
        frontier = [step_id]
        score = 0
        while frontier:
            current = frontier.pop()
            for step in self.steps:
                if step.id in seen:
                    continue
                if current in step.depends_on:
                    seen.add(step.id)
                    score += 1
                    frontier.append(step.id)
        return score

    def get_next_step(self, strict_manifest: bool = True) -> Optional[WorkflowStep]:
        """Get the next step that can be executed."""
        ready = self.ready_steps(strict_manifest=strict_manifest)
        if not ready:
            return None
        if strict_manifest or len(ready) == 1:
            return ready[0]
        ranked = sorted(
            ready,
            key=lambda step: (
                -self._downstream_unlock_score(step.id),
                -len(step.outputs),
                len(step.depends_on),
                step.id,
            ),
        )
        return ranked[0]

    def get_step(self, step_id: str) -> Optional[WorkflowStep]:
        """Get a step by ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def is_complete(self) -> bool:
        """Check if all steps are complete."""
        return all(s.status in (StepStatus.SUCCESS, StepStatus.SKIPPED) for s in self.steps)

    def has_failed(self) -> bool:
        """Check if any step has permanently failed."""
        return any(s.status == StepStatus.FAILED and not s.can_retry() for s in self.steps)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state serialization."""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "workflow_dir": self.workflow_dir,
            "work_dir": self.work_dir,
            "steps": [s.to_dict() for s in self.steps],
            "current_step_id": self.current_step_id,
            "status": self.status,
        }

    def to_plan_steps(self) -> List[Dict[str, Any]]:
        """Convert workflow steps to the generic plan_steps format used by UI/planner."""
        status_map = {
            StepStatus.PENDING: "pending",
            StepStatus.RUNNING: "in_progress",
            StepStatus.SUCCESS: "completed",
            StepStatus.FAILED: "failed",
            StepStatus.SKIPPED: "completed",
        }
        return [
            {
                "id": s.id,
                "description": s.description,
                "type": s.mode or s.engine.value,
                "status": status_map.get(s.status, "pending"),
                "depends_on": s.depends_on,
                **({"planning_source": s.planning_source} if getattr(s, "planning_source", None) else {}),
                **({"orchestration_reason": s.orchestration_reason} if getattr(s, "orchestration_reason", None) else {}),
                **({"outputs": s.outputs} if getattr(s, "outputs", None) else {}),
            }
            for s in self.steps
        ]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowPlan":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            workflow_id=data["workflow_id"],
            workflow_dir=data["workflow_dir"],
            work_dir=data["work_dir"],
            steps=[WorkflowStep.from_dict(s) for s in data.get("steps", [])],
            current_step_id=data.get("current_step_id"),
            status=data.get("status", "draft"),
        )
