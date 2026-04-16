"""
FastAPI Gateway for Renzo Agent
Provides REST API and WebSocket endpoints for the frontend
"""
from __future__ import annotations

import asyncio
import json
import logging
import math
import mimetypes
import os
import queue
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Query, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from controller_events import (
    controller_decision_event,
    controller_guardrail_event,
    controller_legacy_decision_event,
    controller_reply_event,
    run_state_from_result,
)

from dotenv import load_dotenv

_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(_env_path)

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from renzo.app.agent import RenzoAgent
    from renzo.app.state import default_state
    from renzo.app.workflows import (
        WorkflowRunRequest, discover_workflows, get_workflow_by_id,
    )
    from renzo.app.workflows.executor import WorkflowExecutor
    from renzo.app import experiments as exp_mgr
    from renzo.app import datasets as ds_mgr
    from renzo.app import wf_manager
    from renzo.app.shell import ConversationShellManager
    from renzo.app.shell.router import ShellToolRouter
    from renzo.app.shell.rewrite import rewrite_engine_summary_for_humans
    from renzo.app.controller import TopController
    from renzo.app.workflows.onboard import (
        import_workflow_from_github,
        import_workflow_from_zip,
        import_workflow_from_folder,
    )
    from renzo.app.tracing import compact_trace_entries
    from renzo.app.nodes.workflow_run import cleanup_old_workflow_runs
except ImportError:
    sys.path.insert(0, "/app")
    from renzo.app.agent import RenzoAgent
    from renzo.app.state import default_state
    from renzo.app.workflows import (
        WorkflowRunRequest, discover_workflows, get_workflow_by_id,
    )
    from renzo.app.workflows.executor import WorkflowExecutor
    from renzo.app import experiments as exp_mgr
    from renzo.app import datasets as ds_mgr
    from renzo.app import wf_manager
    from renzo.app.shell import ConversationShellManager
    from renzo.app.shell.router import ShellToolRouter
    from renzo.app.shell.rewrite import rewrite_engine_summary_for_humans
    from renzo.app.controller import TopController
    from renzo.app.workflows.onboard import (
        import_workflow_from_github,
        import_workflow_from_zip,
        import_workflow_from_folder,
    )
    from renzo.app.tracing import compact_trace_entries
    from renzo.app.nodes.workflow_run import cleanup_old_workflow_runs

app = FastAPI(title="Renzo API Gateway", version="3.0.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


def _sanitize_for_json(obj: Any) -> Any:
    """Recursively replace NaN/Inf floats with None so JSONResponse doesn't crash."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize_for_json(v) for v in obj]
    return obj


def SafeJSONResponse(content: Any, **kwargs) -> JSONResponse:
    """JSONResponse wrapper that handles NaN/Inf values."""
    return JSONResponse(_sanitize_for_json(content), **kwargs)


def build_api_error(
    code: str,
    message: str,
    hint: str,
    component: str,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a structured API error payload for frontend/ops diagnostics."""
    return {
        "code": code,
        "message": message,
        "hint": hint,
        "component": component,
        "details": details or {},
    }


def raise_api_error(
    status_code: int,
    *,
    code: str,
    message: str,
    hint: str,
    component: str,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    err = build_api_error(code, message, hint, component, details)
    if details is None:
        err["details"] = {}
    err["details"]["retryable"] = status_code in (429, 503)
    raise HTTPException(status_code=status_code, detail=err)


class RateLimiter:
    """In-memory rate limiter: max_requests per window_sec per key."""
    def __init__(self, max_requests: int = 30, window_sec: int = 60):
        self.max_requests = max_requests
        self.window_sec = window_sec
        self._times: Dict[str, List[float]] = {}

    def _prune(self, key: str, now: float) -> None:
        cutoff = now - self.window_sec
        if key in self._times:
            self._times[key] = [t for t in self._times[key] if t > cutoff]
            if not self._times[key]:
                del self._times[key]

    def allow(self, key: str) -> bool:
        now = time.time()
        self._prune(key, now)
        times = self._times.setdefault(key, [])
        if len(times) >= self.max_requests:
            return False
        times.append(now)
        return True


_rate_limiter_chat = RateLimiter(max_requests=30, window_sec=60)
_rate_limiter_ws = RateLimiter(max_requests=60, window_sec=60)


logger = logging.getLogger(__name__)

sessions: Dict[str, Dict] = {}
active_connections: Dict[str, WebSocket] = {}
_hitl_futures: Dict[str, asyncio.Future] = {}
workflow_runs: Dict[str, Dict[str, Any]] = {}
workflow_import_jobs: Dict[str, Dict[str, Any]] = {}
SHELL_ENABLED = os.environ.get("SHELL_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
UNIFIED_CONTROLLER_ENABLED = os.environ.get("UNIFIED_CONTROLLER_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
_shell_manager = ConversationShellManager()
_top_controller = TopController()


def _use_unified_controller(session: Optional[Dict[str, Any]] = None, message: Optional[Dict[str, Any]] = None) -> bool:
    # New explicit override: legacy_shell=true forces legacy path.
    if message and message.get("legacy_shell") is not None:
        return not bool(message.get("legacy_shell"))
    if session and session.get("legacy_shell") is not None:
        return not bool(session.get("legacy_shell"))
    # Backward-compatible override.
    if message and message.get("unified_controller") is not None:
        return bool(message.get("unified_controller"))
    if session and session.get("unified_controller") is not None:
        return bool(session.get("unified_controller"))
    return UNIFIED_CONTROLLER_ENABLED


def _desired_execution_mode_for_session(session: Dict[str, Any]) -> str:
    state = session.get("state") if isinstance(session.get("state"), dict) else {}
    run_mode = str((state or {}).get("run_mode") or "async").strip().lower()
    return "interactive" if run_mode == "stepwise" else "batch"


def _shell_start_experiment_from_workflow(workflow_id: str, req: Dict[str, Any]) -> Dict[str, Any]:
    wf = wf_manager.get_workflow(workflow_id)
    if not wf:
        raise ValueError("Workflow not found")
    ds_ids = req.get("dataset_ids") or wf.get("default_dataset_ids") or []
    exp_name = req.get("name") or f"Experiment: {wf['name']}"
    return exp_mgr.create_experiment(
        name=exp_name,
        description=f"Created from workflow: {wf['name']}",
        dataset_ids=ds_ids,
        tags=["workflow:" + workflow_id],
        workflow_id=workflow_id,
    )


def _shell_link_experiment(exp_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return exp_mgr.update_experiment(
        exp_id,
        workflow_id=updates.get("workflow_id"),
        dataset_ids=updates.get("dataset_ids"),
    )


_shell_manager.configure_router(
    ShellToolRouter(
        list_workflows=lambda: wf_manager.list_workflows(),
        get_workflow=lambda wf_id: wf_manager.get_workflow(wf_id),
        create_workflow=lambda **kwargs: wf_manager.create_workflow(**kwargs),
        start_experiment_from_workflow=_shell_start_experiment_from_workflow,
        list_datasets=lambda: ds_mgr.list_datasets(),
        link_experiment=_shell_link_experiment,
    )
)

_default_data_root = (Path(__file__).resolve().parent.parent / "data").resolve()
DATA_ROOT = Path(os.environ.get("DATA_ROOT", str(_default_data_root))).resolve()
UPLOAD_DIR = DATA_ROOT / "uploads"
WORKFLOW_IMPORTS_DIR = DATA_ROOT / "workflow_imports"
WORKFLOW_IMPORTS_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOW_IMPORT_JOBS_FILE = WORKFLOW_IMPORTS_DIR / "import_jobs.json"
_default_workflow_pool_path = (Path(__file__).resolve().parent.parent / "workflow_pool").resolve()
WORKFLOW_POOL_PATH = Path(os.environ.get("WORKFLOW_POOL_DIR", str(_default_workflow_pool_path))).resolve()


def _load_import_jobs() -> None:
    """Load import jobs from disk into workflow_import_jobs (merge)."""
    if not WORKFLOW_IMPORT_JOBS_FILE.is_file():
        return
    try:
        data = json.loads(WORKFLOW_IMPORT_JOBS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for jid, job in data.items():
                if jid not in workflow_import_jobs:
                    workflow_import_jobs[jid] = job
    except Exception:
        pass


def _save_import_job(job_id: str, job: Dict[str, Any]) -> None:
    """Persist one import job to disk (merge with existing file)."""
    try:
        existing = {}
        if WORKFLOW_IMPORT_JOBS_FILE.is_file():
            existing = json.loads(WORKFLOW_IMPORT_JOBS_FILE.read_text(encoding="utf-8"))
        if not isinstance(existing, dict):
            existing = {}
        existing[job_id] = job
        WORKFLOW_IMPORT_JOBS_FILE.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    except Exception:
        pass
ARTIFACTS_DIR = DATA_ROOT / "artifacts"
WORKFLOWS_DIR = DATA_ROOT / "workflows"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)

WORKFLOW_UPLOAD_EXTENSIONS = {".csv", ".fastq", ".fastq.gz", ".fq", ".fq.gz", ".xlsx", ".xls", ".txt"}

from renzo.app.agent import _STREAM_DONE


class ChatMessage(BaseModel):
    content: str
    session_id: Optional[str] = None
    legacy_shell: Optional[bool] = None
    unified_controller: Optional[bool] = None

class CreateExperimentRequest(BaseModel):
    name: str
    description: str = ""
    dataset_ids: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    workflow_id: Optional[str] = None

class UpdateExperimentRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    dataset_ids: Optional[List[str]] = None
    workflow_id: Optional[str] = None

class CreateDatasetRequest(BaseModel):
    name: str
    description: str = ""
    tags: Optional[List[str]] = None

class UpdateDatasetRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None

class CreateSessionRequest(BaseModel):
    name: str = ""

class CreateWorkflowRequest(BaseModel):
    name: str
    engine: str = "agent"
    description: str = ""
    steps: Optional[List[dict]] = None
    know_how_content: Optional[str] = None
    input_hints: Optional[List[str]] = None
    output_hints: Optional[List[str]] = None

class UpdateWorkflowRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[List[dict]] = None
    engine: Optional[str] = None
    input_hints: Optional[List[str]] = None
    output_hints: Optional[List[str]] = None
    default_dataset_ids: Optional[List[str]] = None

class StartExperimentFromWorkflowRequest(BaseModel):
    name: str = ""
    dataset_ids: Optional[List[str]] = None


class ImportWorkflowRequest(BaseModel):
    source_type: Literal["github", "zip", "folder"]
    github_url: Optional[str] = None
    github_branch: Optional[str] = None
    suggested_id: Optional[str] = None
    path: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Renzo API Gateway", "version": "3.0.0"}


@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health")
async def health_alias():
    """Compatibility alias for environments expecting `/health`."""
    return await health_check()


def _path_readiness(path: Path) -> Dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
    }


def _disk_free_mb(path: Path) -> Optional[int]:
    """Return free space in MB for the filesystem containing path, or None if unavailable."""
    try:
        stat = os.statvfs(path if path.exists() else path.parent)
        return (stat.f_bavail * stat.f_frsize) // (1024 * 1024)
    except (OSError, AttributeError):
        return None


@app.get("/api/ready")
async def readiness_check():
    """Readiness checks for app dependencies and workflow runtime."""
    executor = WorkflowExecutor()
    runtime = executor.get_runtime_status(profile=os.environ.get("WORKFLOW_DEFAULT_PROFILE", "docker"))
    disk_free = _disk_free_mb(DATA_ROOT)
    checks = {
        "app": {"status": "ok"},
        "paths": {
            "data_root": _path_readiness(DATA_ROOT),
            "workflow_pool": _path_readiness(WORKFLOW_POOL_PATH),
        },
        "workflow_runtime": runtime,
        "disk": {
            "data_root_free_mb": disk_free,
            "ok": disk_free is None or disk_free >= 100,
        },
    }

    ready = True
    for item in checks["paths"].values():
        ready = ready and item["exists"] and item["is_dir"] and item["readable"]
    ready = ready and runtime.get("ready", False)
    if checks["disk"].get("ok") is False:
        ready = False

    return JSONResponse(
        {
            "status": "ready" if ready else "degraded",
            "ready": ready,
            "checks": checks,
        }
    )


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), session_id: Optional[str] = None, run_id: Optional[str] = None):
    try:
        if session_id:
            dest_dir = UPLOAD_DIR / session_id
        elif run_id:
            dest_dir = WORKFLOWS_DIR / run_id / "input"
        else:
            dest_dir = UPLOAD_DIR
        dest_dir.mkdir(parents=True, exist_ok=True)
        file_path = dest_dir / (file.filename or "upload")
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        return JSONResponse({"status": "success", "filename": file.filename, "path": str(file_path), "size": len(content)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload/workflow")
async def upload_workflow_files(files: List[UploadFile] = File(...), run_id: Optional[str] = None):
    run_id = run_id or str(uuid.uuid4())
    dest_dir = WORKFLOWS_DIR / run_id / "input"
    dest_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for f in files:
        fn = f.filename or "file"
        fp = dest_dir / fn
        content = await f.read()
        with open(fp, "wb") as out:
            out.write(content)
        paths.append({"filename": fn, "path": str(fp)})
    return JSONResponse({"status": "success", "run_id": run_id, "files": paths})


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@app.post("/api/chat")
async def chat(request: Request, message: ChatMessage):
    ip = _client_ip(request)
    if not _rate_limiter_chat.allow(ip):
        raise_api_error(
            429,
            code="rate_limit_exceeded",
            message="Too many requests. Please try again later.",
            hint="Wait a minute before sending more messages.",
            component="api_gateway",
            details={"retry_after_sec": 60},
        )
    session_id = message.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = {"id": session_id, "created_at": datetime.now().isoformat(), "messages": [], "agent": RenzoAgent(), "state": default_state()}
    session = sessions[session_id]
    if message.legacy_shell is not None:
        session["legacy_shell"] = bool(message.legacy_shell)
    if message.unified_controller is not None:
        session["unified_controller"] = bool(message.unified_controller)
    session["messages"].append({"role": "user", "content": message.content})
    try:
        if _use_unified_controller(
            session,
            {
                "legacy_shell": message.legacy_shell,
                "unified_controller": message.unified_controller,
            },
        ):
            _prepare_agent_context_for_session(session, session_id)
            context = _build_controller_context(session, workflow=None)
            ctrl_out = _top_controller.handle_turn(
                session=session,
                user_input=message.content,
                context=context,
            )
            decision = ctrl_out.get("decision", {})
            _apply_controller_observability(session, decision, controller_path="unified")
            response_content = decision.get("reply", "") or "Ready."
            state_out: Dict[str, Any] = {
                "controller_mode": "unified",
                "controller_phase": decision.get("phase", "dialogue"),
                "controller_trace_id": decision.get("decision_id", ""),
                "pending_guardrail_action": ctrl_out.get("pending_guardrail_action"),
                "risk_level": decision.get("risk_level", "low"),
                "run_state": (session.get("state", {}) or {}).get("run_state", "background"),
                "last_controller_decision": decision,
                "controller_path": "unified",
                "confirm_requested": bool((session.get("state", {}) or {}).get("confirm_requested", False)),
                "confirm_reason_risk": (session.get("state", {}) or {}).get("confirm_reason_risk", ""),
                "loop_guard_triggered": bool((session.get("state", {}) or {}).get("loop_guard_triggered", False)),
                "controller_stats": (session.get("state", {}) or {}).get("controller_stats", {}),
                "shell_state": session.get("shell", {}),
            }
            run_prompt = ctrl_out.get("run_engine_prompt")
            if run_prompt:
                result = session["agent"].go(run_prompt)
                session["state"] = result
                session["state"]["controller_mode"] = "unified"
                session["state"]["controller_phase"] = "executing"
                session["state"]["controller_trace_id"] = decision.get("decision_id", "")
                response_content = rewrite_engine_summary_for_humans(
                    _extract_response(result),
                    workflow_status=result.get("workflow_status", ""),
                    current_step_id=result.get("current_step_id", ""),
                )
                state_out.update(
                    {
                        "plan_status": result.get("plan_status"),
                        "plan_steps": result.get("plan_steps", []),
                        "data_profile": result.get("data_profile", {}),
                        "execution_logs": result.get("execution_logs", []),
                        "qc_results": result.get("qc_results", []),
                        "artifact_index": _compact_artifacts(result.get("artifact_index", [])),
                        "workflow_plan": result.get("workflow_plan"),
                        "workflow_status": result.get("workflow_status"),
                        "workflow_run_id": result.get("workflow_run_id"),
                        "workflow_run_context": result.get("workflow_run_context"),
                        "current_step_id": result.get("current_step_id"),
                        "execution_workdir": result.get("execution_workdir"),
                    }
                )
            session["messages"].append({"role": "assistant", "content": response_content})
            return JSONResponse(
                {
                    "session_id": session_id,
                    "response": response_content,
                    "state": state_out,
                    "controller_trace": ctrl_out.get("trace", {}),
                    "shell_trace": controller_legacy_decision_event(ctrl_out),
                }
            )

        if SHELL_ENABLED:
            _prepare_agent_context_for_session(session, session_id)
            shell_out = _shell_manager.handle_event(
                session,
                event_type="shell_message",
                content=message.content,
                workflow=None,
            )
            _apply_controller_observability(
                session,
                {"requires_confirm": bool((session.get("shell", {}) or {}).get("pending_action")), "risk_level": "low"},
                controller_path="legacy",
            )
            reply = shell_out.get("reply") or {"content": "Ready."}
            run_prompt = shell_out.get("run_engine_prompt")
            response_content = reply.get("content", "")
            shell_trace = shell_out.get("shell_trace", {})
            state_out = {"shell_state": session.get("shell", {})}
            if run_prompt:
                result = session["agent"].go(run_prompt)
                session["state"] = result
                response_content = _shell_manager.rewrite_engine_result(
                    session,
                    engine_text=_extract_response(result),
                    workflow_status=result.get("workflow_status", ""),
                    current_step_id=result.get("current_step_id", ""),
                ).get("content", "")
                artifact_index = result.get("artifact_index", [])
                safe_artifacts = [{k: v for k, v in art.items() if k != "preview" or (v and len(str(v)) < 10000)} for art in artifact_index]
                state_out = {
                    "current_node": result.get("next_node"),
                    "plan_status": result.get("plan_status"),
                    "plan_steps": result.get("plan_steps", []),
                    "data_profile": result.get("data_profile", {}),
                    "execution_logs": result.get("execution_logs", []),
                    "qc_results": result.get("qc_results", []),
                    "artifact_index": safe_artifacts,
                    "workflow_plan": result.get("workflow_plan"),
                    "workflow_status": result.get("workflow_status"),
                    "workflow_run_id": result.get("workflow_run_id"),
                    "workflow_run_context": result.get("workflow_run_context"),
                    "current_step_id": result.get("current_step_id"),
                    "execution_workdir": result.get("execution_workdir"),
                    "shell_state": session.get("shell", {}),
                }
            session["messages"].append({"role": "assistant", "content": response_content})
            return JSONResponse({
                "session_id": session_id,
                "response": response_content,
                "state": state_out,
                "shell_trace": shell_trace,
            })

        result = session["agent"].go(message.content)
        session["state"] = result
        response_content = _extract_response(result)
        session["messages"].append({"role": "assistant", "content": response_content})
        artifact_index = result.get("artifact_index", [])
        safe_artifacts = [{k: v for k, v in art.items() if k != "preview" or (v and len(str(v)) < 10000)} for art in artifact_index]
        return JSONResponse({
            "session_id": session_id,
            "response": response_content,
            "state": {
                "current_node": result.get("next_node"),
                "plan_status": result.get("plan_status"),
                "plan_steps": result.get("plan_steps", []),
                "data_profile": result.get("data_profile", {}),
                "execution_logs": result.get("execution_logs", []),
                "qc_results": result.get("qc_results", []),
                "artifact_index": safe_artifacts,
                "workflow_plan": result.get("workflow_plan"),
                "workflow_status": result.get("workflow_status"),
                "workflow_run_id": result.get("workflow_run_id"),
                "workflow_run_context": result.get("workflow_run_context"),
                "current_step_id": result.get("current_step_id"),
                "execution_workdir": result.get("execution_workdir"),
            },
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _run_workflow_task(run_id, workflow_id, work_dir, params, profile, input_path):
    try:
        base_info = dict(workflow_runs.get(run_id, {}))
        workflow_runs[run_id] = {
            **base_info,
            "run_id": run_id,
            "workflow_id": workflow_id,
            "status": "running",
            "current_step_id": None,
            "step_progress": {"completed": 0, "total": 1},
            "error_summary": "",
            "error_details": None,
            "artifact_count": 0,
        }
        wf = get_workflow_by_id(workflow_id)
        if not wf:
            error_detail = build_api_error(
                "workflow_not_found",
                f"Workflow {workflow_id} was not found.",
                "Verify workflow_id and configured workflow discovery roots.",
                "workflow_runtime",
                {"workflow_id": workflow_id, "workflow_pool": str(WORKFLOW_POOL_PATH)},
            )
            workflow_runs[run_id] = {
                **workflow_runs[run_id],
                "status": "failed",
                "error_summary": error_detail["message"],
                "error_details": error_detail,
            }
            return
        ex = WorkflowExecutor()
        if wf.engine == "nextflow":
            nf_params = {k: v for k, v in params.items() if k != "config"}
            result = ex.run_nextflow(workflow_path=wf.path, work_dir=work_dir, params=nf_params, profile=profile, input_path=input_path)
        elif wf.engine == "snakemake":
            result = ex.run_snakemake(workflow_path=wf.path, work_dir=work_dir, params=params, use_singularity=(profile == "singularity"), config=params.get("config"))
        else:
            error_detail = build_api_error(
                "unsupported_engine",
                f"Unsupported engine: {wf.engine}",
                "Use a workflow with engine 'nextflow', 'snakemake', or 'agent'.",
                "workflow_runtime",
                {"workflow_id": workflow_id, "engine": wf.engine},
            )
            workflow_runs[run_id] = {
                **workflow_runs[run_id],
                "status": "failed",
                "error_summary": error_detail["message"],
                "error_details": error_detail,
            }
            return
        result_error_detail = result.error_detail or {}
        workflow_runs[run_id] = {
            **base_info,
            "run_id": run_id,
            "workflow_id": workflow_id,
            "status": "success" if result.status == "success" else "failed",
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
            "returncode": result.returncode,
            "output_paths": result.output_paths or [],
            "work_dir": result.work_dir or str(work_dir),
            "start_ts": result.start_ts,
            "end_ts": result.end_ts,
            "current_step_id": None,
            "step_progress": {"completed": 1 if result.status == "success" else 0, "total": 1},
            "error_summary": "" if result.status == "success" else (result.error or result.stderr or "Workflow run failed"),
            "error_details": None if result.status == "success" else result_error_detail,
            "artifact_count": len(result.output_paths or []),
        }
    except Exception as e:
        base_info = dict(workflow_runs.get(run_id, {}))
        error_detail = build_api_error(
            "workflow_task_exception",
            "Unexpected exception while executing workflow task.",
            "Inspect backend logs for stack trace details.",
            "workflow_runtime",
            {"exception": str(e), "workflow_id": workflow_id},
        )
        workflow_runs[run_id] = {
            **base_info,
            "run_id": run_id,
            "workflow_id": workflow_id,
            "status": "failed",
            "current_step_id": None,
            "step_progress": {"completed": 0, "total": 1},
            "error_summary": error_detail["message"],
            "error_details": error_detail,
            "artifact_count": 0,
        }

@app.get("/api/workflows")
async def list_workflows_endpoint():
    try:
        return JSONResponse({"workflows": wf_manager.list_workflows()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflows")
async def create_workflow_endpoint(req: CreateWorkflowRequest):
    try:
        result = wf_manager.create_workflow(
            name=req.name, engine=req.engine, description=req.description,
            steps=req.steps, know_how_content=req.know_how_content,
            input_hints=req.input_hints, output_hints=req.output_hints,
        )
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflows/import/{job_id}")
async def get_workflow_import_job_endpoint(job_id: str):
    if job_id not in workflow_import_jobs:
        _load_import_jobs()
    if job_id not in workflow_import_jobs:
        raise HTTPException(status_code=404, detail="Import job not found")
    info = dict(workflow_import_jobs[job_id])
    return JSONResponse(info)


@app.post("/api/workflows/import")
async def import_workflow_endpoint(
    background_tasks: BackgroundTasks,
    source_type: Literal["github", "zip", "folder"] = Form(...),
    github_url: Optional[str] = Form(None),
    github_branch: Optional[str] = Form(None),
    suggested_id: Optional[str] = Form(None),
    path: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """Start a workflow import job. Returns 202 with job_id and status_url for polling."""
    if source_type == "zip" and file and file.filename and file.filename.lower().endswith(".zip"):
        zip_path = WORKFLOW_IMPORTS_DIR / f"{uuid.uuid4().hex}.zip"
        content = await file.read()
        zip_path.write_bytes(content)
        path = str(zip_path)
    job_id = str(uuid.uuid4())
    workflow_import_jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "workflow_id": None,
        "name": None,
        "engine": None,
        "error": None,
        "created_at": datetime.now().isoformat(),
    }
    _save_import_job(job_id, workflow_import_jobs[job_id])
    background_tasks.add_task(
        _run_workflow_import_task,
        job_id,
        source_type,
        github_url,
        github_branch,
        path,
        suggested_id,
    )
    return JSONResponse(
        status_code=202,
        content={
            "job_id": job_id,
            "status_url": f"/api/workflows/import/{job_id}",
            "status": "queued",
        },
    )


@app.get("/api/workflows/{workflow_id}")
async def get_workflow_endpoint(workflow_id: str):
    wf = wf_manager.get_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return JSONResponse(wf)

@app.put("/api/workflows/{workflow_id}")
async def update_workflow_endpoint(workflow_id: str, req: UpdateWorkflowRequest):
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    result = wf_manager.update_workflow(workflow_id, updates)
    if not result:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return JSONResponse(result)

@app.delete("/api/workflows/{workflow_id}")
async def delete_workflow_endpoint(workflow_id: str):
    if not wf_manager.delete_workflow(workflow_id):
        raise HTTPException(status_code=404, detail="Workflow not found")
    return JSONResponse({"status": "deleted", "id": workflow_id})


def _run_workflow_import_task(job_id: str, source_type: str, github_url: Optional[str], github_branch: Optional[str], path: Optional[str], suggested_id: Optional[str]):
    """Background task: run onboard pipeline and update workflow_import_jobs[job_id]."""
    workflow_import_jobs[job_id]["status"] = "running"
    _save_import_job(job_id, workflow_import_jobs[job_id])
    try:
        if source_type == "github":
            if not github_url:
                raise ValueError("github_url required for source_type=github")
            result = import_workflow_from_github(
                url=github_url,
                branch=github_branch or "main",
                suggested_id=suggested_id,
                pool_path=WORKFLOW_POOL_PATH,
            )
        elif source_type == "zip":
            if not path:
                raise ValueError("path required for source_type=zip")
            result = import_workflow_from_zip(
                zip_path=path,
                suggested_id=suggested_id,
                pool_path=WORKFLOW_POOL_PATH,
            )
        elif source_type == "folder":
            if not path:
                raise ValueError("path required for source_type=folder")
            result = import_workflow_from_folder(
                folder_path=path,
                suggested_id=suggested_id,
                pool_path=WORKFLOW_POOL_PATH,
            )
        else:
            raise ValueError(f"Unsupported source_type: {source_type}")
        workflow_import_jobs[job_id]["status"] = "success"
        workflow_import_jobs[job_id]["workflow_id"] = result.get("workflow_id")
        workflow_import_jobs[job_id]["name"] = result.get("name")
        workflow_import_jobs[job_id]["engine"] = result.get("engine")
        _save_import_job(job_id, workflow_import_jobs[job_id])
    except Exception as e:
        workflow_import_jobs[job_id]["status"] = "failed"
        workflow_import_jobs[job_id]["error"] = str(e)
        _save_import_job(job_id, workflow_import_jobs[job_id])


@app.get("/api/workflows/{workflow_id}/know-how")
async def get_workflow_know_how_endpoint(workflow_id: str):
    content = wf_manager.get_workflow_know_how(workflow_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Know-how not found")
    return JSONResponse({"workflow_id": workflow_id, "content": content})

@app.post("/api/workflows/{workflow_id}/start-experiment")
async def start_experiment_from_workflow(workflow_id: str, req: StartExperimentFromWorkflowRequest):
    """Create an experiment pre-linked to a workflow's datasets and know-how."""
    wf = wf_manager.get_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail="Workflow not found")
    ds_ids = req.dataset_ids or wf.get("default_dataset_ids") or []
    exp_name = req.name or f"Experiment: {wf['name']}"
    try:
        meta = exp_mgr.create_experiment(
            name=exp_name,
            description=f"Created from workflow: {wf['name']}",
            dataset_ids=ds_ids,
            tags=["workflow:" + workflow_id],
            workflow_id=workflow_id,
        )
        return JSONResponse(meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflows/run")
async def run_workflow(req: WorkflowRunRequest, background_tasks: BackgroundTasks):
    wf = get_workflow_by_id(req.workflow_id)
    if not wf:
        raise_api_error(
            404,
            code="workflow_not_found",
            message="Workflow not found.",
            hint="Verify workflow_id and configured workflow discovery roots.",
            component="workflow_api",
            details={"workflow_id": req.workflow_id, "workflow_pool": str(WORKFLOW_POOL_PATH)},
        )

    run_id = str(uuid.uuid4())
    requested_mode = (req.execution_mode or "").strip().lower()
    execution_mode = requested_mode or ("interactive" if wf.engine == "agent" else "batch")
    strict_manifest = True if req.strict_manifest is None else bool(req.strict_manifest)
    artifact_policy = (req.artifact_policy or "session").strip().lower()

    # Agent workflows run through experiment/session chat execution.
    if wf.engine == "agent":
        exp_id = req.experiment_id
        if exp_id and not exp_mgr.get_experiment(exp_id):
            raise_api_error(
                404,
                code="experiment_not_found",
                message=f"Experiment not found: {exp_id}",
                hint="Create the experiment first or omit experiment_id for auto-create.",
                component="workflow_api",
                details={"experiment_id": exp_id},
            )
        if not exp_id:
            exp_meta = exp_mgr.create_experiment(
                name=f"Workflow Run: {wf.name}",
                description=f"Auto-created run container for workflow {wf.id}",
                dataset_ids=list(wf.default_dataset_ids or []),
                tags=[f"workflow:{wf.id}"],
                workflow_id=wf.id,
            )
            exp_id = exp_meta["id"]

        sess_id = req.session_id
        if sess_id and not exp_mgr.get_session(exp_id, sess_id):
            raise_api_error(
                404,
                code="session_not_found",
                message=f"Session not found: {sess_id}",
                hint="Use an existing session_id or omit session_id for auto-create.",
                component="workflow_api",
                details={"experiment_id": exp_id, "session_id": sess_id},
            )
        if not sess_id:
            session_meta = exp_mgr.create_session(exp_id, name=f"Run: {wf.name}")
            if not session_meta:
                raise_api_error(
                    500,
                    code="session_create_failed",
                    message="Failed to create workflow session.",
                    hint="Inspect backend logs and experiment store permissions.",
                    component="workflow_api",
                    details={"experiment_id": exp_id, "workflow_id": wf.id},
                )
            sess_id = session_meta["id"]

        workflow_runs[run_id] = {
            "run_id": run_id,
            "workflow_id": wf.id,
            "status": "queued",
            "current_step_id": None,
            "step_progress": {"completed": 0, "total": len(wf.steps or [])},
            "error_summary": "",
            "error_details": None,
            "artifact_count": 0,
            "experiment_id": exp_id,
            "session_id": sess_id,
            "execution_mode": execution_mode,
            "strict_manifest": strict_manifest,
            "artifact_policy": artifact_policy,
            "status_url": f"/api/workflows/runs/{run_id}",
        }
        return JSONResponse({
            "run_id": run_id,
            "workflow_id": wf.id,
            "status": "queued",
            "experiment_id": exp_id,
            "session_id": sess_id,
            "execution_mode": execution_mode,
            "strict_manifest": strict_manifest,
            "artifact_policy": artifact_policy,
            "status_url": f"/api/workflows/runs/{run_id}",
        })

    # Non-agent workflows keep background task execution.
    work_dir = WORKFLOWS_DIR / run_id
    work_dir.mkdir(parents=True, exist_ok=True)
    input_path = None
    if req.input_paths:
        inp = req.input_paths.get("input") or req.input_paths.get("samplesheet")
        if inp:
            input_path = inp
        elif "input_dir" in req.input_paths:
            input_path = req.input_paths["input_dir"]
    params = dict(req.params or {})
    workflow_runs[run_id] = {
        "run_id": run_id,
        "workflow_id": wf.id,
        "status": "queued",
        "current_step_id": None,
        "step_progress": {"completed": 0, "total": 1},
        "error_summary": "",
        "error_details": None,
        "artifact_count": 0,
        "experiment_id": req.experiment_id,
        "session_id": req.session_id,
        "execution_mode": execution_mode,
        "strict_manifest": strict_manifest,
        "artifact_policy": artifact_policy,
        "status_url": f"/api/workflows/runs/{run_id}",
    }
    background_tasks.add_task(
        _run_workflow_task,
        run_id,
        req.workflow_id,
        work_dir,
        params,
        req.profile or "docker",
        input_path,
    )
    return JSONResponse({
        "run_id": run_id,
        "workflow_id": req.workflow_id,
        "status": "queued",
        "work_dir": str(work_dir),
        "experiment_id": req.experiment_id,
        "session_id": req.session_id,
        "execution_mode": execution_mode,
        "strict_manifest": strict_manifest,
        "artifact_policy": artifact_policy,
        "status_url": f"/api/workflows/runs/{run_id}",
    })

@app.get("/api/workflows/runs/{run_id}")
async def get_workflow_run(run_id: str):
    if run_id not in workflow_runs:
        raise_api_error(
            404,
            code="run_not_found",
            message="Run not found.",
            hint="Use /api/workflows/run to create a run first.",
            component="workflow_api",
            details={"run_id": run_id},
        )
    run_info = dict(workflow_runs[run_id])

    # Agent runs expose live status from persisted session state.
    if run_info.get("experiment_id") and run_info.get("session_id"):
        sess = exp_mgr.get_session(run_info["experiment_id"], run_info["session_id"])
        if sess and isinstance(sess.get("agent_state"), dict):
            agent_state = sess["agent_state"]
            run_ctx = agent_state.get("workflow_run_context")
            if not isinstance(run_ctx, dict):
                run_ctx = {}
            wf_plan = agent_state.get("workflow_plan") or {}
            wf_steps = wf_plan.get("steps") if isinstance(wf_plan, dict) else []
            completed = run_info.get("step_progress", {}).get("completed", 0)
            total = run_info.get("step_progress", {}).get("total", 0)
            if wf_steps:
                completed = 0
                total = len(wf_steps)
                for s in wf_steps:
                    if s.get("status") in ("success", "skipped"):
                        completed += 1
            artifacts = agent_state.get("artifact_index") or []
            run_info.update({
                "status": run_ctx.get("status") or agent_state.get("workflow_status") or run_info.get("status"),
                "current_step_id": (
                    run_ctx.get("current_step_id")
                    or agent_state.get("current_step_id")
                    or run_info.get("current_step_id")
                ),
                "step_progress": {"completed": completed, "total": total},
                "artifact_count": len(artifacts),
                "error_summary": (
                    run_ctx.get("error_summary")
                    or
                    (agent_state.get("validation_result") or {}).get("stderr_excerpt", "")
                    or run_info.get("error_summary", "")
                ),
            })

    return JSONResponse(run_info)


@app.get("/api/sessions")
async def list_in_memory_sessions():
    return JSONResponse({"sessions": [{"id": sid, "created_at": s["created_at"], "message_count": len(s["messages"])} for sid, s in sessions.items()]})

@app.get("/api/sessions/{session_id}")
async def get_in_memory_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    return JSONResponse({"session_id": session_id, "created_at": session["created_at"], "messages": session["messages"], "state": session.get("state", {})})

@app.delete("/api/sessions/{session_id}")
async def delete_in_memory_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    del sessions[session_id]
    return JSONResponse({"status": "deleted", "session_id": session_id})


def _build_dataset_context(dataset_ids: list) -> str:
    """Resolve dataset IDs to file paths and build a structured context string."""
    lines = ["=== AVAILABLE DATASETS ==="]
    for ds_id in dataset_ids:
        meta = ds_mgr.get_dataset(ds_id)
        if not meta:
            continue
        files_dir = ds_mgr.get_dataset_files_dir(ds_id)
        if not files_dir:
            continue
        files = sorted(f.name for f in files_dir.iterdir() if f.is_file() and not f.name.startswith("."))
        lines.append(f'\n[{ds_id}] "{meta.get("name", ds_id)}"')
        if meta.get("description"):
            desc = meta["description"]
            if len(desc) > 200:
                desc = desc[:200] + "..."
            lines.append(f"  Description: {desc}")
        lines.append(f"  Directory: {files_dir}")
        lines.append(f"  Files ({len(files)}): {', '.join(files)}")
    if len(lines) <= 1:
        return ""
    lines.append("\nIMPORTANT: Use the absolute directory paths above when reading data files.")
    lines.append("For example: read.csv(file.path(\"<directory>\", \"dm.csv\")) in R")
    lines.append("         or: pd.read_csv(os.path.join(\"<directory>\", \"dm.csv\")) in Python")
    lines.append("=== END DATASETS ===")
    return "\n".join(lines)


def _build_linked_dataset_summary(dataset_ids: list) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for ds_id in (dataset_ids or []):
        try:
            meta = ds_mgr.get_dataset(ds_id)
        except Exception:
            meta = None
        if not meta:
            items.append({"id": ds_id, "name": ds_id, "file_count": 0, "description": ""})
            continue
        items.append(
            {
                "id": meta.get("id", ds_id),
                "name": meta.get("name", ds_id),
                "file_count": meta.get("file_count", 0),
                "description": meta.get("description", ""),
            }
        )
    return items


def _apply_controller_observability(session: Dict[str, Any], decision: Dict[str, Any], *, controller_path: str) -> None:
    state = session.setdefault("state", {})
    stats = dict(state.get("controller_stats") or {})
    stats["controller_path"] = controller_path
    stats["total_decisions"] = int(stats.get("total_decisions", 0) or 0) + 1
    requires_confirm = bool(decision.get("requires_confirm", False))
    stats["confirm_requested"] = requires_confirm
    stats["confirm_reason_risk"] = decision.get("risk_level", "low") if requires_confirm else ""
    stats["confirm_request_count"] = int(stats.get("confirm_request_count", 0) or 0) + (1 if requires_confirm else 0)
    loop_guard_triggered = bool(decision.get("state_patch", {}).get("loop_guard_triggered", False))
    stats["loop_guard_triggered"] = loop_guard_triggered
    stats["loop_guard_trigger_count"] = int(stats.get("loop_guard_trigger_count", 0) or 0) + (1 if loop_guard_triggered else 0)
    state["controller_stats"] = stats
    state["controller_path"] = controller_path
    state["confirm_requested"] = requires_confirm
    state["confirm_reason_risk"] = stats["confirm_reason_risk"]
    state["loop_guard_triggered"] = loop_guard_triggered


def _build_controller_context(session: Dict[str, Any], workflow: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    linked_datasets = session.get("linked_datasets") or []
    linked_dataset_ids = [d.get("id") for d in linked_datasets if isinstance(d, dict) and d.get("id")]
    linked_dataset_names = [d.get("name") for d in linked_datasets if isinstance(d, dict) and d.get("name")]
    state = session.get("state") or {}
    return {
        "experiment_id": session.get("experiment_id"),
        "session_id": session.get("session_id"),
        "linked_workflow_id": (workflow or {}).get("id") or "",
        "linked_workflow_name": (workflow or {}).get("name") or "",
        "linked_workflow_steps": [s.get("name") or s.get("id") for s in ((workflow or {}).get("steps") or [])][:8],
        "linked_dataset_ids": linked_dataset_ids,
        "linked_dataset_names": linked_dataset_names[:12],
        "linked_dataset_count": len(linked_dataset_ids),
        "plan_status": state.get("plan_status", ""),
        "workflow_status": state.get("workflow_status", ""),
        "controller_phase": state.get("controller_phase", "dialogue"),
        "controller_path": state.get("controller_path", "unified"),
        "confirm_requested": bool(state.get("confirm_requested", False)),
        "confirm_reason_risk": state.get("confirm_reason_risk", ""),
        "loop_guard_triggered": bool(state.get("loop_guard_triggered", False)),
        "user_agent_mode": state.get("user_agent_mode", "ask"),
    }


def _extract_response(result):
    response_content = "Analysis complete"
    messages = result.get("messages", [])
    if messages:
        for msg in reversed(messages):
            content = getattr(msg, "content", None)
            if content and getattr(msg, "type", "") == "ai":
                response_content = content
                break
    if response_content == "Analysis complete" and result.get("execution_logs"):
        latest_log = result["execution_logs"][-1]
        response_content = latest_log.get("stdout", "No output")
    return response_content


def _truncate_text(value: Any, max_len: int) -> Any:
    """Truncate for persistence/compact state only; keeps start of string so user sees beginning."""
    if isinstance(value, str) and len(value) > max_len:
        return value[:max_len]
    return value


def _compact_execution_logs(logs: Any, max_logs: int = 50, max_text_len: int = 4000) -> list:
    if not isinstance(logs, list):
        return []
    compacted = []
    for raw in logs[-max_logs:]:
        if not isinstance(raw, dict):
            continue
        entry = dict(raw)
        entry["stdout"] = _truncate_text(entry.get("stdout"), max_text_len)
        entry["stderr"] = _truncate_text(entry.get("stderr"), max_text_len)
        compacted.append(entry)
    return compacted


def _compact_artifacts(artifacts: Any, max_preview_len: int = 4000) -> list:
    if not isinstance(artifacts, list):
        return []
    compacted = []
    for raw in artifacts:
        if not isinstance(raw, dict):
            continue
        art = dict(raw)
        preview = art.get("preview")
        if isinstance(preview, str) and len(preview) > max_preview_len:
            art["preview"] = preview[:max_preview_len]
        compacted.append(art)
    return compacted


def _compact_agent_state_for_client(state: Any) -> Dict[str, Any]:
    if not isinstance(state, dict):
        return {}
    compacted = dict(state)
    compacted["execution_logs"] = _compact_execution_logs(compacted.get("execution_logs"))
    compacted["artifact_index"] = _compact_artifacts(compacted.get("artifact_index"))
    compacted["code_scratchpad"] = _truncate_text(compacted.get("code_scratchpad"), 20000)
    compacted["llm_trace"] = compact_trace_entries(compacted.get("llm_trace"))
    compacted["orchestration_trace"] = compact_trace_entries(compacted.get("orchestration_trace"))
    return compacted


def _compact_messages_for_client(messages: Any, max_messages: int = 200, max_text_len: int = 100_000) -> list:
    if not isinstance(messages, list):
        return []
    compacted = []
    for raw in messages[-max_messages:]:
        if not isinstance(raw, dict):
            continue
        msg = dict(raw)
        msg["content"] = _truncate_text(msg.get("content"), max_text_len)
        compacted.append(msg)
    return compacted


def _hydrate_ws_session_from_disk(session: Dict[str, Any], ws_session_id: str) -> None:
    """Load persisted experiment session state into in-memory websocket session once."""
    exp_id = session.get("experiment_id")
    sess_id = session.get("session_id")
    if not exp_id or not sess_id:
        return

    bound_key = f"{exp_id}:{sess_id}"
    if session.get("_hydrated_key") == bound_key:
        return

    persisted = exp_mgr.get_session_hydrated(exp_id, sess_id)
    if not isinstance(persisted, dict):
        session["_hydrated_key"] = bound_key
        return

    persisted_state = persisted.get("agent_state")
    if isinstance(persisted_state, dict) and persisted_state:
        merged_state = default_state()
        merged_state.update(persisted_state)
        merged_state["experiment_id"] = exp_id
        merged_state["session_id"] = sess_id
        session["state"] = merged_state
        session["agent"].state = dict(merged_state)

    persisted_messages = persisted.get("messages")
    if isinstance(persisted_messages, list):
        session["messages"] = persisted_messages

    session["_hydrated_key"] = bound_key


def _maybe_persist_session(session: Dict[str, Any], *, force: bool = False, min_interval_s: float = 1.0) -> None:
    """Persist session periodically during streaming so mid-run progress survives refresh."""
    now = time.monotonic()
    last = float(session.get("_last_persist_ts", 0.0) or 0.0)
    if not force and (now - last) < min_interval_s:
        return
    _persist_session(session)
    session["_last_persist_ts"] = now


async def _ws_send_safe(websocket: WebSocket, data: dict):
    """Send JSON over websocket, sanitizing NaN/Inf to avoid serialization crashes."""
    try:
        await websocket.send_json(_sanitize_for_json(data))
    except Exception as e:
        logger.warning("Failed to send WS message: %s", e)


async def _stream_agent_to_ws(websocket, agent, prompt, session):
    q = queue.Queue()
    loop = asyncio.get_event_loop()
    prev_node = None
    cancel_event = threading.Event()
    session["agent_cancel_event"] = cancel_event
    thread = threading.Thread(
        target=agent.stream_to_queue,
        args=(prompt, q),
        kwargs={"cancel_event": cancel_event},
        daemon=True,
    )
    thread.start()
    while True:
        try:
            snapshot = await asyncio.wait_for(loop.run_in_executor(None, q.get, True, 0.5), timeout=120)
        except (asyncio.TimeoutError, Exception):
            if not thread.is_alive():
                break
            continue
        if snapshot is _STREAM_DONE:
            break
        if snapshot.get("_stream_error"):
            await _ws_send_safe(websocket, {"type": "error", "message": snapshot["_stream_error"]})
            break
        session["state"] = snapshot
        _maybe_persist_session(session)
        cur_node = snapshot.get("current_node") or snapshot.get("next_node")
        if cur_node and cur_node != prev_node:
            await _ws_send_safe(websocket, {"type": "node_change", "node": cur_node})
            prev_node = cur_node
        if snapshot.get("plan_steps"):
            await _ws_send_safe(websocket, {"type": "plan_update", "plan_steps": snapshot["plan_steps"], "plan_status": snapshot.get("plan_status")})
        if snapshot.get("code_scratchpad"):
            await _ws_send_safe(websocket, {"type": "code_update", "code": snapshot["code_scratchpad"], "language": snapshot.get("code_language", "python")})
        if snapshot.get("execution_logs"):
            latest = snapshot["execution_logs"][-1] if snapshot["execution_logs"] else None
            if latest:
                await _ws_send_safe(
                    websocket,
                    {
                        "type": "execution_update",
                        "log": {
                            "run_id": latest.get("run_id"),
                            "workflow_id": latest.get("workflow_id"),
                            "step_id": latest.get("step_id"),
                            "status": latest.get("status", "running"),
                            "language": latest.get("language", "python"),
                            "stdout": (latest.get("stdout") or "")[-500:],
                            "stderr": (latest.get("stderr") or "")[-300:],
                            "artifact_count": latest.get("artifact_count", 0),
                        },
                    },
                )
        qc_results = snapshot.get("qc_results", [])
        if qc_results:
            await _ws_send_safe(websocket, {"type": "qc_result", "qc_summary": qc_results[-1]})
        artifact_index = snapshot.get("artifact_index", [])
        if artifact_index:
            safe_artifacts = [{k: v for k, v in art.items() if k != "preview" or (v and len(str(v)) < 10000)} for art in artifact_index]
            await _ws_send_safe(websocket, {"type": "artifact_new", "artifacts": safe_artifacts})
        if snapshot.get("hitl_pending"):
            break
    thread.join(timeout=5)
    _maybe_persist_session(session, force=True)
    return session["state"]


async def _stream_agent_hitl_resume(websocket, agent, hitl_response, session):
    q = queue.Queue()
    loop = asyncio.get_event_loop()
    prev_node = None
    thread = threading.Thread(target=agent.resume_after_hitl_to_queue, args=(hitl_response, q), daemon=True)
    thread.start()
    while True:
        try:
            snapshot = await asyncio.wait_for(loop.run_in_executor(None, q.get, True, 0.5), timeout=120)
        except (asyncio.TimeoutError, Exception):
            if not thread.is_alive():
                break
            continue
        if snapshot is _STREAM_DONE:
            break
        if snapshot.get("_stream_error"):
            await _ws_send_safe(websocket, {"type": "error", "message": snapshot["_stream_error"]})
            break
        session["state"] = snapshot
        _maybe_persist_session(session)
        cur_node = snapshot.get("current_node") or snapshot.get("next_node")
        if cur_node and cur_node != prev_node:
            await _ws_send_safe(websocket, {"type": "node_change", "node": cur_node})
            prev_node = cur_node
        if snapshot.get("plan_steps"):
            await _ws_send_safe(websocket, {"type": "plan_update", "plan_steps": snapshot["plan_steps"], "plan_status": snapshot.get("plan_status")})
        if snapshot.get("code_scratchpad"):
            await _ws_send_safe(websocket, {"type": "code_update", "code": snapshot["code_scratchpad"], "language": snapshot.get("code_language", "python")})
        if snapshot.get("execution_logs"):
            latest = snapshot["execution_logs"][-1] if snapshot["execution_logs"] else None
            if latest:
                await _ws_send_safe(
                    websocket,
                    {
                        "type": "execution_update",
                        "log": {
                            "run_id": latest.get("run_id"),
                            "workflow_id": latest.get("workflow_id"),
                            "step_id": latest.get("step_id"),
                            "status": latest.get("status", "running"),
                            "language": latest.get("language", "python"),
                            "stdout": (latest.get("stdout") or "")[-500:],
                            "stderr": (latest.get("stderr") or "")[-300:],
                            "artifact_count": latest.get("artifact_count", 0),
                        },
                    },
                )
        qc_results = snapshot.get("qc_results", [])
        if qc_results:
            await _ws_send_safe(websocket, {"type": "qc_result", "qc_summary": qc_results[-1]})
        artifact_index = snapshot.get("artifact_index", [])
        if artifact_index:
            safe_artifacts = [{k: v for k, v in art.items() if k != "preview" or (v and len(str(v)) < 10000)} for art in artifact_index]
            await _ws_send_safe(websocket, {"type": "artifact_new", "artifacts": safe_artifacts})
        if snapshot.get("hitl_pending"):
            break
    thread.join(timeout=5)
    _maybe_persist_session(session, force=True)
    return session["state"]


def _apply_reset_to_step(session: Dict[str, Any], target_step_id: str) -> bool:
    """Reset target step and all later steps to pending, clearing associated
    execution data so the step re-runs cleanly.

    Clears: plan step statuses, execution_logs, qc_results, artifact_index
    entries for the reset steps, retry/error state, and session messages.
    Updates both session['state'] and session['agent'].state.
    Returns True if applied.
    """
    if not target_step_id or not target_step_id.strip():
        logger.warning("reset_to_step: empty target_step_id")
        return False
    target_step_id = target_step_id.strip()
    state = session.get("state") or {}
    plan_steps = state.get("plan_steps") or []
    if not plan_steps:
        logger.warning(
            "reset_to_step: plan_steps is empty. exp=%s sess=%s hydrated=%s state_keys=%s",
            session.get("experiment_id"), session.get("session_id"),
            session.get("_hydrated_key"), sorted(state.keys())[:15],
        )
        return False

    step_ids = [(s.get("id") or "") for s in plan_steps if isinstance(s, dict)]
    reset_step_ids: set = set()
    found = False
    for s in plan_steps:
        if isinstance(s, dict) and (s.get("id") or "").strip() == target_step_id:
            found = True
        if found:
            s["status"] = "pending"
            reset_step_ids.add((s.get("id") or "").strip())
    if not found:
        logger.warning(
            "reset_to_step: target %r not found in plan_steps ids=%s",
            target_step_id, step_ids,
        )
        return False

    # --- Reset plan metadata ---
    state["plan_steps"] = plan_steps
    state["plan_status"] = "executing"
    state["workflow_status"] = state.get("workflow_status") or "executing"
    state["current_step_id"] = target_step_id

    run_ctx = dict(state.get("workflow_run_context") or {})
    run_ctx["status"] = "running"
    run_ctx["ended_at"] = None
    state["workflow_run_context"] = run_ctx

    # --- Keep logs/artifacts from earlier steps, remove only reset steps' data ---
    old_logs = state.get("execution_logs") or []
    state["execution_logs"] = [
        lg for lg in old_logs
        if (lg.get("step_id") or "") not in reset_step_ids
    ]
    old_qc = state.get("qc_results") or []
    state["qc_results"] = [
        qc for qc in old_qc
        if (qc.get("step_id") or "") not in reset_step_ids
    ]
    state["retry_count"] = 0
    state["validation_result"] = {}
    state["error_book"] = []
    state["code_scratchpad"] = ""

    old_artifacts = state.get("artifact_index") or []
    state["artifact_index"] = [
        a for a in old_artifacts
        if (a.get("step_id") or "") not in reset_step_ids
    ]

    session["state"] = state
    # Keep session messages — they contain earlier steps' conversation history.

    # --- Mirror into live agent state ---
    agent_state = getattr(session.get("agent"), "state", None)
    if isinstance(agent_state, dict):
        agent_state["plan_steps"] = list(plan_steps)
        agent_state["plan_status"] = "executing"
        agent_state["workflow_status"] = state.get("workflow_status")
        agent_state["current_step_id"] = target_step_id
        agent_state["workflow_run_context"] = dict(run_ctx)
        agent_state["execution_logs"] = list(state["execution_logs"])
        agent_state["qc_results"] = list(state["qc_results"])
        agent_state["retry_count"] = 0
        agent_state["validation_result"] = {}
        agent_state["error_book"] = []
        agent_state["code_scratchpad"] = ""
        agent_state["artifact_index"] = list(state["artifact_index"])

    # --- Reset workflow_plan step objects ---
    plan_data = state.get("workflow_plan")
    if isinstance(plan_data, dict):
        steps = plan_data.get("steps") or []
        wf_found = False
        for s in steps:
            if isinstance(s, dict) and (s.get("id") or "").strip() == target_step_id:
                wf_found = True
            if wf_found:
                s["status"] = "pending"
                s["retry_count"] = 0
                s["error"] = None
        plan_data["status"] = "executing"
        plan_data["current_step_id"] = target_step_id
        state["workflow_plan"] = plan_data
        session["state"] = state
        if isinstance(agent_state, dict):
            agent_state["workflow_plan"] = dict(plan_data)
    return True


def _prepare_agent_context_for_session(
    session: Dict[str, Any],
    ws_session_id: str,
) -> Dict[str, Any]:
    """Bind experiment/session/workflow context to the agent state."""
    exp_meta: Dict[str, Any] = {}
    # Apply user-preferred code language (python / r) for coder and executor
    session["agent"].state["code_language"] = session.get("state", {}).get("user_code_language", "python")
    if session.get("experiment_id"):
        session["agent"].state["experiment_id"] = session["experiment_id"]
        if session.get("session_id"):
            session["agent"].state["session_id"] = session["session_id"]
        exp_meta = exp_mgr.get_experiment(session["experiment_id"]) or {}
        if exp_meta.get("workflow_id"):
            wf_id = exp_meta["workflow_id"]
            session["agent"].load_workflow_know_how(wf_id)
            # Bind workflow execution context explicitly for strict manifest runs.
            session["agent"].state["workflow_id_requested"] = wf_id
            run_ctx = dict(session["agent"].state.get("workflow_run_context") or {})
            run_ctx.setdefault("run_id", f"wf-{wf_id}-{(session.get('session_id') or ws_session_id)[:8]}")
            run_ctx.setdefault("workflow_id", wf_id)
            run_ctx.setdefault("engine", "agent")
            run_ctx["experiment_id"] = session["experiment_id"]
            run_ctx["session_id"] = session.get("session_id")
            if _use_unified_controller(session):
                run_ctx["execution_mode"] = _desired_execution_mode_for_session(session)
            else:
                run_ctx.setdefault("execution_mode", "interactive")
            run_ctx.setdefault("strict_manifest", True)
            run_ctx.setdefault("status", "queued")
            run_ctx.setdefault("current_step_id", None)
            run_ctx.setdefault("started_at", datetime.now().isoformat())
            run_ctx.setdefault("ended_at", None)
            run_ctx.setdefault("error_summary", "")
            session["agent"].state["workflow_run_context"] = run_ctx
            session["agent"].state["workflow_run_id"] = run_ctx.get("run_id")
            session["agent"].state["artifact_policy"] = (
                session["agent"].state.get("artifact_policy") or "session"
            )
            exec_dir = exp_mgr.resolve_execution_workdir(
                session["experiment_id"],
                session.get("session_id"),
                session["agent"].state["artifact_policy"],
            )
            exec_dir.mkdir(parents=True, exist_ok=True)
            session["agent"].state["execution_workdir"] = str(exec_dir)
        # Resolve linked datasets to file paths and inject context
        if exp_meta.get("dataset_ids"):
            session["linked_datasets"] = _build_linked_dataset_summary(exp_meta["dataset_ids"])
            ds_context = _build_dataset_context(exp_meta["dataset_ids"])
            if ds_context:
                session["agent"].state["dataset_context"] = ds_context
        else:
            session["linked_datasets"] = []
    if session.get("session_id"):
        session["agent"].state["session_id"] = session["session_id"]
    session["agent"].state["run_mode"] = str((session.get("state") or {}).get("run_mode") or "async")
    session["agent"].state.setdefault("controller_mode", "legacy")
    session["agent"].state.setdefault("controller_phase", "dialogue")
    session["agent"].state.setdefault("run_mode", "async")
    session["agent"].state.setdefault("run_state", "background")
    session["agent"].state.setdefault("pending_guardrail_action", None)
    session["agent"].state.setdefault("risk_level", "low")
    session["agent"].state.setdefault("last_controller_decision", {})
    session["agent"].state.setdefault("conversation_loop_count", 0)
    session["agent"].state.setdefault("controller_trace_id", "")
    session["agent"].state.setdefault("controller_path", "unified")
    session["agent"].state.setdefault("confirm_requested", False)
    session["agent"].state.setdefault("confirm_reason_risk", "")
    session["agent"].state.setdefault("loop_guard_triggered", False)
    session["agent"].state.setdefault("controller_stats", {})
    return exp_meta


def _engine_prompt_with_user_intent(controller_prompt: str, user_message: str) -> str:
    """Ensure the experiment agent receives the user's exact request so dialogue and engine stay connected.
    If the controller shortened or rephrased the prompt, we prepend the user's words so the agent has full context.
    """
    user = (user_message or "").strip()
    prompt = (controller_prompt or "").strip()
    if not user:
        return prompt or "continue"
    if not prompt or prompt == user or user in prompt:
        return prompt or user
    return f"User request: {user}\n\nExecute: {prompt}"


async def _execute_engine_turn(
    websocket: WebSocket,
    session: Dict[str, Any],
    ws_session_id: str,
    prompt: str,
    *,
    emit_assistant_message: bool = True,
    user_message: Optional[str] = None,
) -> Dict[str, Any]:
    """Run one engine turn and stream state updates; returns result payload."""
    content = _engine_prompt_with_user_intent(prompt, user_message or prompt)
    # Prepend user-selected mode so planner can respect ask/plan/execute/data_analysis
    mode = (session.get("state") or {}).get("user_agent_mode", "ask")
    if mode and mode in ("ask", "plan", "execute", "data_analysis"):
        content = f"[Mode: {mode}]\n\n{content}"
    exp_meta = _prepare_agent_context_for_session(session, ws_session_id)
    # Prepend dataset context to prompt on first message only.
    if exp_meta.get("dataset_ids"):
        ds_context = session["agent"].state.get("dataset_context")
        if ds_context and len(session.get("messages", [])) <= 1:
            content = f"{ds_context}\n\n{content}"

    result = await _stream_agent_to_ws(websocket, session["agent"], content, session)
    if result.get("hitl_pending"):
        await _ws_send_safe(websocket, {"type": "hitl_request", "question": result.get("hitl_question", ""), "context": result.get("hitl_context", ""), "reason": result.get("hitl_reason", "")})
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        _hitl_futures[ws_session_id] = future
        try:
            human_response = await asyncio.wait_for(future, timeout=600)
        except asyncio.TimeoutError:
            human_response = "[HITL timeout]"
        finally:
            _hitl_futures.pop(ws_session_id, None)
        session["state"]["hitl_response"] = human_response
        session["state"]["hitl_pending"] = False
        result = await _stream_agent_hitl_resume(websocket, session["agent"], human_response, session)

    response_content = _extract_response(result)
    response_attachments = result.get("response_attachments", []) or []
    suggested_mode = result.get("suggested_mode")
    if emit_assistant_message:
        session["messages"].append({
            "role": "assistant",
            "content": response_content,
            "attachments": response_attachments,
            "suggested_mode": suggested_mode,
        })
        payload = {"type": "message", "role": "assistant", "content": response_content, "attachments": response_attachments}
        if suggested_mode:
            payload["suggested_mode"] = suggested_mode
        await _ws_send_safe(websocket, payload)

    artifact_index = result.get("artifact_index", [])
    session.setdefault("state", {})
    session["state"]["run_state"] = run_state_from_result(result)
    compact_state = {
        "plan_status": result.get("plan_status"),
        "plan_steps": result.get("plan_steps", []),
        "data_profile": result.get("data_profile", {}),
        "execution_logs": _compact_execution_logs(result.get("execution_logs", [])),
        "qc_results": result.get("qc_results", []),
        "code_scratchpad": _truncate_text(result.get("code_scratchpad"), 20000),
        "code_language": result.get("code_language", "python"),
        "artifact_index": _compact_artifacts(artifact_index),
        "experiment_id": session.get("experiment_id"),
        "session_id": session.get("session_id"),
        "workflow_plan": result.get("workflow_plan"),
        "workflow_status": result.get("workflow_status"),
        "workflow_run_id": result.get("workflow_run_id"),
        "workflow_run_context": result.get("workflow_run_context"),
        "current_step_id": result.get("current_step_id"),
        "execution_workdir": result.get("execution_workdir"),
        "llm_trace": compact_trace_entries(
            result.get("llm_trace", (session.get("state", {}) or {}).get("llm_trace"))
        ),
        "orchestration_trace": compact_trace_entries(
            result.get("orchestration_trace", (session.get("state", {}) or {}).get("orchestration_trace"))
        ),
        "controller_mode": result.get("controller_mode", (session.get("state", {}) or {}).get("controller_mode", "legacy")),
        "controller_phase": result.get("controller_phase", (session.get("state", {}) or {}).get("controller_phase", "dialogue")),
        "run_state": run_state_from_result(result),
        "pending_guardrail_action": (session.get("state", {}) or {}).get("pending_guardrail_action"),
        "risk_level": (session.get("state", {}) or {}).get("risk_level", "low"),
        "last_controller_decision": (session.get("state", {}) or {}).get("last_controller_decision", {}),
        "controller_trace_id": (session.get("state", {}) or {}).get("controller_trace_id", ""),
        "controller_path": (session.get("state", {}) or {}).get("controller_path", "unified"),
        "confirm_requested": bool((session.get("state", {}) or {}).get("confirm_requested", False)),
        "confirm_reason_risk": (session.get("state", {}) or {}).get("confirm_reason_risk", ""),
        "loop_guard_triggered": bool((session.get("state", {}) or {}).get("loop_guard_triggered", False)),
        "controller_stats": (session.get("state", {}) or {}).get("controller_stats", {}),
        "shell_state": session.get("shell", {}),
        "shell_trace": {
            "trace_id": (session.get("shell", {}) or {}).get("last_trace_id", ""),
            "phase": (session.get("shell", {}) or {}).get("phase", "execution"),
            "intent": (session.get("shell", {}) or {}).get("last_intent", ""),
            "tool_calls": (session.get("shell", {}) or {}).get("last_tool_calls", []),
            "requires_confirm": bool((session.get("shell", {}) or {}).get("pending_action")),
            "fallback_used": bool((session.get("shell", {}) or {}).get("fallback_used", False)),
        },
    }
    await _ws_send_safe(websocket, {"type": "complete", "state": compact_state})
    await _ws_send_safe(
        websocket,
        {
            "type": "run_state_changed",
            "run_state": run_state_from_result(result),
            "workflow_status": result.get("workflow_status", ""),
            "plan_status": result.get("plan_status", ""),
            "current_step_id": result.get("current_step_id", ""),
        },
    )
    await _ws_send_safe(
        websocket,
        {
            "type": "controller_progress",
            "plan_status": result.get("plan_status", ""),
            "workflow_status": result.get("workflow_status", ""),
            "current_step_id": result.get("current_step_id", ""),
            "artifact_count": len(artifact_index),
        },
    )
    # Merge result into session state so persist saves updated plan_steps (e.g. step completed after retry)
    session["state"].update(compact_state)
    _maybe_persist_session(session, force=True)
    return {
        "result": result,
        "response_content": response_content,
        "response_attachments": response_attachments,
        "response_qc_table": result.get("response_qc_table") or [],
    }


@app.websocket("/ws/{ws_session_id}")
async def websocket_endpoint(websocket: WebSocket, ws_session_id: str):
    await websocket.accept()
    active_connections[ws_session_id] = websocket
    if ws_session_id not in sessions:
        sessions[ws_session_id] = {"id": ws_session_id, "created_at": datetime.now().isoformat(), "messages": [], "agent": RenzoAgent(), "state": default_state(), "experiment_id": None, "session_id": None}
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type", "message")
            session = sessions[ws_session_id]
            # Interrupt: set cancel event so agent thread can exit at next step boundary (if running).
            if msg_type == "shell_control" and message.get("command") in ("stop", "interrupt"):
                ev = session.get("agent_cancel_event")
                if ev:
                    ev.set()
                await _ws_send_safe(websocket, {"type": "run_state_changed", "run_state": "stopped", "message": "Interrupt requested."})
                continue
            if msg_type == "hitl_response":
                human_response = message.get("response", "")
                # Guardrail confirmation via HITL: run the pending engine turn after user confirms.
                pending = session.get("pending_guardrail") or {}
                run_prompt = pending.pop("run_prompt", None)
                user_message = pending.pop("user_message", "")
                if pending:
                    session["pending_guardrail"] = pending
                else:
                    session.pop("pending_guardrail", None)
                if run_prompt is not None:
                    if human_response and human_response.strip().lower() not in ("no", "cancel", "n"):
                        await _execute_engine_turn(
                            websocket,
                            session,
                            ws_session_id,
                            run_prompt,
                            emit_assistant_message=False,
                            user_message=user_message,
                        )
                    else:
                        await _ws_send_safe(websocket, {"type": "message", "role": "assistant", "content": "Action canceled. You can ask for something else when ready."})
                        session["messages"].append({"role": "assistant", "content": "Action canceled."})
                        await _ws_send_safe(websocket, {"type": "complete", "state": {"confirm_requested": False}})
                    continue
                # Agent graph HITL (planner/QC asked a question).
                future = _hitl_futures.pop(ws_session_id, None)
                if future and not future.done():
                    future.set_result(human_response)
                else:
                    session["state"]["hitl_response"] = human_response
                    session["state"]["hitl_pending"] = False
                continue
            content = message.get("content", "")
            if message.get("experiment_id"):
                session["experiment_id"] = message["experiment_id"]
            if message.get("session_id"):
                session["session_id"] = message["session_id"]
            if message.get("legacy_shell") is not None:
                session["legacy_shell"] = bool(message.get("legacy_shell"))
            if message.get("unified_controller") is not None:
                session["unified_controller"] = bool(message.get("unified_controller"))
            _hydrate_ws_session_from_disk(session, ws_session_id)
            trace_id = (session.get("state") or {}).get("controller_trace_id") or ""
            logger.info("WS message session_id=%s trace_id=%s type=%s", ws_session_id, trace_id or "(none)", msg_type, extra={"ws_session_id": ws_session_id, "trace_id": trace_id})
            if msg_type in {"message", "shell_message"}:
                if not _rate_limiter_ws.allow(ws_session_id):
                    await _ws_send_safe(websocket, {
                        "type": "error",
                        "message": "Too many messages. Please wait a moment before sending more.",
                        "code": "rate_limit_exceeded",
                        "retryable": True,
                    })
                    continue
                session["messages"].append({"role": "user", "content": content})
                await _ws_send_safe(websocket, {"type": "message", "role": "user", "content": content})
                # Persist user-selected agent mode (ask / plan / analysis) for controller and planner
                mode = (message.get("agent_mode") or "ask").strip().lower()
                if mode == "data_analysis":
                    mode = "analysis"
                if mode in ("ask", "plan", "analysis"):
                    session.setdefault("state", {})["user_agent_mode"] = mode
                # Persist preferred code language (python / r) for planner and coder
                code_lang = (message.get("code_language") or "python").strip().lower()
                if code_lang in ("python", "r"):
                    session.setdefault("state", {})["user_code_language"] = code_lang
            # If we are waiting for HITL and user sent a message, treat it as the HITL response (e.g. they replied in main input).
            if msg_type in {"message", "shell_message"} and content.strip():
                future = _hitl_futures.get(ws_session_id)
                if future is not None and not future.done():
                    _hitl_futures.pop(ws_session_id, None)
                    future.set_result(content.strip())
                    continue
            try:
                if _use_unified_controller(session, message) and msg_type in {"shell_message", "message", "guardrail_confirm", "shell_action_confirm"}:
                    _prepare_agent_context_for_session(session, ws_session_id)
                    workflow = None
                    if session.get("experiment_id"):
                        exp_meta = exp_mgr.get_experiment(session["experiment_id"]) or {}
                        wf_id = exp_meta.get("workflow_id")
                        if wf_id:
                            try:
                                workflow = wf_manager.get_workflow(wf_id)
                            except Exception:
                                workflow = None

                    ctrl_out: Dict[str, Any]
                    if msg_type in {"shell_message", "message"}:
                        ctrl_out = _top_controller.handle_turn(
                            session=session,
                            user_input=content,
                            context=_build_controller_context(session, workflow),
                        )
                    else:
                        decision_id = str(message.get("decision_id") or message.get("action_id") or "").strip()
                        ctrl_out = _top_controller.handle_guardrail_confirm(
                            session=session,
                            decision_id=decision_id,
                            approved=bool(message.get("approved", False)),
                            edits=message.get("edits") if isinstance(message.get("edits"), dict) else None,
                        )
                        if ctrl_out.get("error"):
                            await _ws_send_safe(websocket, {"type": "error", "message": ctrl_out.get("reply", "Invalid guardrail confirmation.")})
                            continue
                        # Keep event payload shape aligned with handle_turn output.
                        decision_stub = {
                            "decision_id": decision_id,
                            "phase": (session.get("state", {}) or {}).get("controller_phase", "dialogue"),
                            "action": {"type": "execute_step" if ctrl_out.get("run_engine_prompt") else "ask_user"},
                            "risk_level": (session.get("state", {}) or {}).get("risk_level", "low"),
                            "requires_confirm": False,
                            "reply": ctrl_out.get("reply", ""),
                            "reasoning_brief": "Guardrail confirmation handled.",
                            "fallback_used": False,
                            "run_engine_prompt": ctrl_out.get("run_engine_prompt"),
                        }
                        ctrl_out = {
                            "decision": decision_stub,
                            "trace": {
                                "trace_id": decision_id,
                                "phase": decision_stub["phase"],
                                "action": decision_stub["action"]["type"],
                                "risk_level": decision_stub["risk_level"],
                                "requires_confirm": False,
                                "fallback_used": False,
                            },
                            "run_engine_prompt": ctrl_out.get("run_engine_prompt"),
                            "pending_guardrail_action": (session.get("state", {}) or {}).get("pending_guardrail_action"),
                        }

                    _apply_controller_observability(session, ctrl_out.get("decision", {}), controller_path="unified")
                    decision_event = controller_decision_event(ctrl_out)
                    legacy_decision_event = controller_legacy_decision_event(ctrl_out)
                    reply_event = controller_reply_event(ctrl_out)
                    guardrail_event = controller_guardrail_event(ctrl_out)
                    run_prompt = ctrl_out.get("run_engine_prompt")
                    if not (run_prompt and str(run_prompt).strip()) and content and str(content).strip():
                        run_prompt = content.strip()
                    decision = ctrl_out.get("decision", {})
                    requires_confirm = bool(decision.get("requires_confirm", False))
                    emit_pre_execution_reply = not bool(run_prompt) or requires_confirm

                    await _ws_send_safe(websocket, decision_event)
                    await _ws_send_safe(websocket, legacy_decision_event)
                    if emit_pre_execution_reply:
                        await _ws_send_safe(websocket, reply_event)
                        session["messages"].append({"role": "assistant", "content": reply_event.get("content", "")})
                    if guardrail_event:
                        await _ws_send_safe(websocket, guardrail_event)
                        await _ws_send_safe(
                            websocket,
                            {
                                "type": "shell_plan_proposal",
                                "action_id": guardrail_event.get("decision_id", ""),
                                "title": guardrail_event.get("title", ""),
                                "summary": guardrail_event.get("summary", ""),
                                "steps": ["Review guardrail action", "Confirm to execute"],
                                "risks": [f"Risk level: {guardrail_event.get('risk_level', 'low')}"],
                                "requires_confirm": True,
                            },
                        )
                    # Use HITL for guardrail confirmation so one unified human-in-the-loop flow.
                    if run_prompt and requires_confirm:
                        session.setdefault("pending_guardrail", {})
                        session["pending_guardrail"]["run_prompt"] = run_prompt
                        session["pending_guardrail"]["user_message"] = content
                        session["pending_guardrail"]["decision_id"] = decision.get("decision_id", "")
                        await _ws_send_safe(
                            websocket,
                            {
                                "type": "hitl_request",
                                "question": (guardrail_event or {}).get("summary", "Confirm to execute this step?"),
                                "context": (guardrail_event or {}).get("title", "Guardrail confirmation"),
                                "reason": "Confirm to run the planned action.",
                            },
                        )
                        run_prompt = None  # do not run engine until user confirms via hitl_response

                    session.setdefault("state", {})
                    session["state"]["controller_mode"] = "unified"
                    session["state"]["last_controller_decision"] = ctrl_out.get("decision", {})
                    session["state"]["controller_trace_id"] = (ctrl_out.get("decision", {}) or {}).get("decision_id", "")
                    if run_prompt:
                        engine_out = await _execute_engine_turn(
                            websocket,
                            session,
                            ws_session_id,
                            run_prompt,
                            emit_assistant_message=False,
                            user_message=content,
                        )
                        result = engine_out["result"]
                        response_content = engine_out.get("response_content", "")
                        short_status = rewrite_engine_summary_for_humans(
                            response_content,
                            workflow_status=result.get("workflow_status", ""),
                            current_step_id=result.get("current_step_id", ""),
                        )
                        await _ws_send_safe(
                            websocket,
                            {
                                "type": "controller_progress",
                                "plan_status": result.get("plan_status", ""),
                                "workflow_status": result.get("workflow_status", ""),
                                "current_step_id": result.get("current_step_id", ""),
                                "artifact_count": len(result.get("artifact_index", []) or []),
                                "summary": short_status,
                            },
                        )
                        # Send the full response as the chat reply so the user sees the complete analysis, not a truncation.
                        plan_steps = result.get("plan_steps") or []
                        has_pending_steps = any(
                            isinstance(s, dict) and s.get("status") in ("pending", "in_progress")
                            for s in plan_steps
                        )
                        compat_reply = {
                            "type": "shell_reply",
                            "content": response_content or short_status,
                            "tone": "professional",
                            "concise": False,
                            "chips": ["Continue"] if has_pending_steps else [],
                            "pending_action": None,
                            "phase": "executing",
                            "trace_id": session["state"].get("controller_trace_id", ""),
                            "attachments": engine_out.get("response_attachments", []) or [],
                        }
                        if engine_out.get("response_qc_table"):
                            compat_reply["qc_table"] = engine_out["response_qc_table"]
                        await _ws_send_safe(websocket, compat_reply)
                        session["messages"].append({
                            "role": "assistant",
                            "content": compat_reply["content"],
                            "attachments": compat_reply.get("attachments", []),
                            "qc_table": compat_reply.get("qc_table") or [],
                        })
                    else:
                        await _ws_send_safe(
                            websocket,
                            {
                                "type": "complete",
                                "state": {
                                    "controller_mode": "unified",
                                    "controller_phase": (ctrl_out.get("decision", {}) or {}).get("phase", "dialogue"),
                                    "run_state": "background",
                                    "pending_guardrail_action": ctrl_out.get("pending_guardrail_action"),
                                    "risk_level": (ctrl_out.get("decision", {}) or {}).get("risk_level", "low"),
                                    "last_controller_decision": ctrl_out.get("decision", {}),
                                    "controller_trace": ctrl_out.get("trace", {}),
                                    "controller_path": (session.get("state", {}) or {}).get("controller_path", "unified"),
                                    "confirm_requested": bool((session.get("state", {}) or {}).get("confirm_requested", False)),
                                    "confirm_reason_risk": (session.get("state", {}) or {}).get("confirm_reason_risk", ""),
                                    "loop_guard_triggered": bool((session.get("state", {}) or {}).get("loop_guard_triggered", False)),
                                    "controller_stats": (session.get("state", {}) or {}).get("controller_stats", {}),
                                },
                            },
                        )
                    continue

                # Legacy shell protocol (feature-flagged). Legacy "message" is also
                # routed through shell when enabled.
                if SHELL_ENABLED and msg_type in {"shell_message", "message", "shell_action_confirm", "shell_control", "shell_tool_result_ack", "shell_retry_last"}:
                    _prepare_agent_context_for_session(session, ws_session_id)
                    workflow = None
                    if session.get("experiment_id"):
                        exp_meta = exp_mgr.get_experiment(session["experiment_id"]) or {}
                        wf_id = exp_meta.get("workflow_id")
                        if wf_id:
                            try:
                                workflow = wf_manager.get_workflow(wf_id)
                            except Exception:
                                workflow = None

                    shell_out: Dict[str, Any]
                    if msg_type in {"shell_message", "message"}:
                        shell_out = _shell_manager.handle_event(
                            session,
                            event_type="shell_message",
                            content=content,
                            workflow=workflow,
                        )
                    elif msg_type == "shell_action_confirm":
                        shell_out = _shell_manager.handle_event(
                            session,
                            event_type="shell_action_confirm",
                            action_id=message.get("action_id", ""),
                            approved=bool(message.get("approved", False)),
                            edits=message.get("edits") if isinstance(message.get("edits"), dict) else None,
                            workflow=workflow,
                        )
                    elif msg_type == "shell_control":
                        cmd = (message.get("command") or "").strip().lower()
                        target_step_id = message.get("target_step_id")
                        if cmd == "reset_to_step":
                            if not target_step_id:
                                await _ws_send_safe(websocket, {"type": "error", "message": "Cannot reset: no step selected."})
                                continue
                            _hydrate_ws_session_from_disk(session, ws_session_id)
                            if _apply_reset_to_step(session, str(target_step_id)):
                                await _ws_send_safe(websocket, {
                                    "type": "plan_update",
                                    "plan_steps": session["state"].get("plan_steps"),
                                    "plan_status": "executing",
                                    "current_step_id": session["state"].get("current_step_id"),
                                })
                                await _ws_send_safe(websocket, {
                                    "type": "step_reset",
                                    "target_step_id": str(target_step_id),
                                    "artifact_index": session["state"].get("artifact_index") or [],
                                    "execution_logs": _compact_execution_logs(session["state"].get("execution_logs") or []),
                                    "qc_results": session["state"].get("qc_results") or [],
                                })
                                _maybe_persist_session(session, force=True)
                                await _execute_engine_turn(
                                    websocket, session, ws_session_id,
                                    "continue",
                                    emit_assistant_message=True,
                                )
                            else:
                                await _ws_send_safe(websocket, {"type": "error", "message": "Could not reset to this step. Plan may be empty or step not found."})
                            continue
                        shell_out = _shell_manager.handle_event(
                            session,
                            event_type="shell_control",
                            command=cmd or message.get("command", ""),
                            target_step_id=target_step_id if cmd != "continue" else None,
                            reason=message.get("reason", ""),
                            workflow=workflow,
                        )
                    elif msg_type == "shell_retry_last":
                        shell_out = _shell_manager.handle_event(
                            session,
                            event_type="shell_retry_last",
                            workflow=workflow,
                        )
                    else:
                        shell_out = _shell_manager.handle_event(
                            session,
                            event_type="shell_tool_result_ack",
                            trace_id=message.get("trace_id", ""),
                        )
                    _apply_controller_observability(
                        session,
                        {"requires_confirm": bool((session.get("shell", {}) or {}).get("pending_action")), "risk_level": "low"},
                        controller_path="legacy",
                    )

                    session.setdefault("state", {})
                    session["state"]["shell_state"] = session.get("shell", {})

                    if shell_out.get("decision_event"):
                        await _ws_send_safe(websocket, shell_out["decision_event"])
                    if shell_out.get("reply"):
                        await _ws_send_safe(websocket, shell_out["reply"])
                        session["messages"].append({"role": "assistant", "content": shell_out["reply"].get("content", "")})
                    if shell_out.get("proposal"):
                        await _ws_send_safe(websocket, shell_out["proposal"])
                    if shell_out.get("memory_hint"):
                        await _ws_send_safe(websocket, shell_out["memory_hint"])

                    run_prompt = shell_out.get("run_engine_prompt")
                    if run_prompt:
                        engine_out = await _execute_engine_turn(
                            websocket,
                            session,
                            ws_session_id,
                            run_prompt,
                            emit_assistant_message=False,
                            user_message=content if msg_type in ("shell_message", "message") else None,
                        )
                        result = engine_out["result"]
                        shell_reply = _shell_manager.rewrite_engine_result(
                            session,
                            engine_text=engine_out["response_content"],
                            workflow_status=result.get("workflow_status", ""),
                            current_step_id=result.get("current_step_id", ""),
                        )
                        # Send full reply content for display (do not use summarized rewrite)
                        shell_reply["content"] = engine_out.get("response_content", "") or shell_reply.get("content", "")
                        shell_reply["attachments"] = engine_out.get("response_attachments", []) or []
                        qc_table = engine_out.get("response_qc_table") or []
                        if qc_table:
                            shell_reply["qc_table"] = qc_table
                        await _ws_send_safe(websocket, shell_reply)
                        session["messages"].append({
                            "role": "assistant",
                            "content": shell_reply["content"],
                            "attachments": shell_reply.get("attachments", []),
                            "qc_table": shell_reply.get("qc_table") or [],
                        })
                    else:
                        await _ws_send_safe(
                            websocket,
                            {
                                "type": "complete",
                                "state": {
                                    "shell_state": session.get("shell", {}),
                                    "shell_trace": shell_out.get("shell_trace", {}),
                                },
                            },
                        )
                    continue

                # Legacy path when shell is disabled.
                await _execute_engine_turn(
                    websocket,
                    session,
                    ws_session_id,
                    content,
                    emit_assistant_message=True,
                    user_message=content,
                )
            except Exception as e:
                logger.error("WebSocket handler error: %s", e, exc_info=True)
                await _ws_send_safe(websocket, {"type": "error", "message": str(e)})
    except WebSocketDisconnect:
        session = sessions.get(ws_session_id)
        if isinstance(session, dict):
            _maybe_persist_session(session, force=True)
        _hitl_futures.pop(ws_session_id, None)
        active_connections.pop(ws_session_id, None)


def _persist_session(session):
    exp_id = session.get("experiment_id")
    sess_id = session.get("session_id")
    if not exp_id or not sess_id:
        return
    try:
        exp_mgr.save_session_state(exp_id, sess_id, messages=session.get("messages", []), agent_state=session.get("state", {}))
    except Exception as e:
        logger.warning("Failed to persist session state: %s", e)


@app.get("/api/sessions/{session_id}/artifacts")
async def get_session_artifacts(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    state = sessions[session_id].get("state", {})
    artifacts = state.get("artifact_index", [])
    safe = [{k: v for k, v in a.items() if k != "preview"} for a in artifacts]
    return JSONResponse({"session_id": session_id, "artifacts": safe})

@app.get("/api/sessions/{session_id}/artifacts/{artifact_id}")
async def get_artifact_detail(session_id: str, artifact_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    state = sessions[session_id].get("state", {})
    for art in state.get("artifact_index", []):
        if art.get("id") == artifact_id:
            return JSONResponse(art)
    raise HTTPException(status_code=404, detail="Artifact not found")

@app.get("/api/sessions/{session_id}/plan")
async def get_session_plan(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    state = sessions[session_id].get("state", {})
    return JSONResponse({"session_id": session_id, "plan_version": state.get("plan_version", 0), "plan_status": state.get("plan_status", "unknown"), "plan_steps": state.get("plan_steps", []), "qc_results": state.get("qc_results", [])})


@app.post("/api/datasets")
async def create_dataset(req: CreateDatasetRequest):
    try:
        meta = ds_mgr.create_dataset(name=req.name, description=req.description, tags=req.tags)
        return JSONResponse(meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/datasets")
async def list_datasets(status: Optional[str] = None):
    return JSONResponse({"datasets": ds_mgr.list_datasets(status=status)})

@app.get("/api/datasets/{ds_id}")
async def get_dataset(ds_id: str):
    meta = ds_mgr.get_dataset(ds_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return JSONResponse(meta)

@app.put("/api/datasets/{ds_id}")
async def update_dataset(ds_id: str, req: UpdateDatasetRequest):
    meta = ds_mgr.update_dataset(ds_id, name=req.name, description=req.description, status=req.status, tags=req.tags)
    if not meta:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return JSONResponse(meta)

@app.delete("/api/datasets/{ds_id}")
async def delete_dataset(ds_id: str):
    if not ds_mgr.delete_dataset(ds_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    return JSONResponse({"status": "deleted", "id": ds_id})

@app.get("/api/datasets/{ds_id}/files")
async def list_dataset_files(ds_id: str):
    meta = ds_mgr.get_dataset(ds_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return JSONResponse({"dataset_id": ds_id, "files": ds_mgr.list_dataset_files(ds_id)})

@app.post("/api/datasets/{ds_id}/files")
async def upload_dataset_file(ds_id: str, file: UploadFile = File(...)):
    meta = ds_mgr.get_dataset(ds_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Dataset not found")
    try:
        content = await file.read()
        result = ds_mgr.save_dataset_file(ds_id, file.filename or "upload", content)
        return JSONResponse({"status": "success", **result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/datasets/{ds_id}/files/download")
async def download_dataset_file(ds_id: str, path: str = ""):
    if not path:
        raise HTTPException(status_code=400, detail="path parameter required")
    file_path = ds_mgr.get_dataset_file_path(ds_id, path)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(file_path), filename=file_path.name, media_type="application/octet-stream")


@app.get("/api/datasets/{ds_id}/files/serve")
async def serve_dataset_file(ds_id: str, path: str = ""):
    """Serve a dataset file with proper MIME type for inline preview."""
    if not path:
        raise HTTPException(status_code=400, detail="path parameter required")
    file_path = ds_mgr.get_dataset_file_path(ds_id, path)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        ext = file_path.suffix.lower()
        mime_map = {
            ".csv": "text/csv", ".tsv": "text/tab-separated-values",
            ".json": "application/json", ".txt": "text/plain", ".log": "text/plain",
            ".md": "text/markdown", ".html": "text/html", ".htm": "text/html",
            ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp",
            ".pdf": "application/pdf", ".xpt": "application/octet-stream",
            ".xls": "application/vnd.ms-excel", ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".rds": "application/octet-stream", ".rda": "application/octet-stream",
        }
        mime_type = mime_map.get(ext, "application/octet-stream")
    return FileResponse(path=str(file_path), media_type=mime_type)


@app.get("/api/datasets/{ds_id}/files/preview")
async def preview_dataset_file(ds_id: str, path: str = "", max_lines: int = 200):
    """Return text content of a dataset file for preview (CSV, TSV, TXT, JSON, etc.)."""
    if not path:
        raise HTTPException(status_code=400, detail="path parameter required")
    file_path = ds_mgr.get_dataset_file_path(ds_id, path)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    ext = file_path.suffix.lower()
    size = file_path.stat().st_size

    # Binary files — no text preview
    if ext in {".xpt", ".rds", ".rda", ".pdf", ".xls", ".xlsx", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}:
        return JSONResponse({
            "type": "binary",
            "ext": ext,
            "size": size,
            "message": f"Binary file ({ext}), {size} bytes. Use download or serve endpoint.",
        })

    # Text-based files — read and return
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line.rstrip("\n"))
        return JSONResponse({
            "type": "text",
            "ext": ext,
            "size": size,
            "total_lines_shown": len(lines),
            "truncated": len(lines) >= max_lines,
            "content": "\n".join(lines),
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cannot read file: {e}")


@app.delete("/api/datasets/{ds_id}/files")
async def delete_dataset_file(ds_id: str, filename: str = ""):
    if not filename:
        raise HTTPException(status_code=400, detail="filename parameter required")
    if not ds_mgr.delete_dataset_file(ds_id, filename):
        raise HTTPException(status_code=404, detail="File not found")
    return JSONResponse({"status": "deleted", "filename": filename})


@app.post("/api/experiments")
async def create_experiment(req: CreateExperimentRequest):
    try:
        meta = exp_mgr.create_experiment(name=req.name, description=req.description, dataset_ids=req.dataset_ids, tags=req.tags, workflow_id=req.workflow_id)
        return JSONResponse(meta)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/experiments/{exp_id}/duplicate")
async def duplicate_experiment(exp_id: str):
    """Duplicate an experiment (metadata only, no sessions)."""
    meta = exp_mgr.duplicate_experiment(exp_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return JSONResponse(meta)

@app.get("/api/experiments")
async def list_experiments(status: Optional[str] = None):
    return JSONResponse({"experiments": exp_mgr.list_experiments(status=status)})

@app.get("/api/experiments/{exp_id}")
async def get_experiment(exp_id: str):
    meta = exp_mgr.get_experiment(exp_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return JSONResponse(meta)

@app.put("/api/experiments/{exp_id}")
async def update_experiment(exp_id: str, req: UpdateExperimentRequest):
    meta = exp_mgr.update_experiment(exp_id, name=req.name, description=req.description, status=req.status, tags=req.tags, dataset_ids=req.dataset_ids, workflow_id=req.workflow_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return JSONResponse(meta)

@app.delete("/api/experiments/{exp_id}")
async def delete_experiment(exp_id: str):
    if not exp_mgr.delete_experiment(exp_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return JSONResponse({"status": "deleted", "id": exp_id})


@app.post("/api/experiments/{exp_id}/sessions")
async def create_experiment_session(exp_id: str, req: CreateSessionRequest):
    meta = exp_mgr.get_experiment(exp_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Experiment not found")
    session = exp_mgr.create_session(exp_id, name=req.name)
    if not session:
        raise HTTPException(status_code=500, detail="Failed to create session")
    return JSONResponse(session)

@app.get("/api/experiments/{exp_id}/sessions")
async def list_experiment_sessions(exp_id: str):
    meta = exp_mgr.get_experiment(exp_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return JSONResponse({"experiment_id": exp_id, "sessions": exp_mgr.list_sessions(exp_id)})

@app.get("/api/experiments/{exp_id}/sessions/{sess_id}")
async def get_experiment_session(exp_id: str, sess_id: str):
    session = exp_mgr.get_session_hydrated(exp_id, sess_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    agent_state = _compact_agent_state_for_client(session.get("agent_state", {}))
    agent_state["experiment_id"] = exp_id
    agent_state["session_id"] = sess_id
    response_data = {
        **session,
        "messages": _compact_messages_for_client(session.get("messages", [])),
        "agent_state": agent_state,
    }
    return SafeJSONResponse(response_data)


@app.get("/api/experiments/{exp_id}/sessions/{sess_id}/memory")
async def get_experiment_session_memory_index(exp_id: str, sess_id: str):
    session = exp_mgr.get_session(exp_id, sess_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    manifest = exp_mgr.get_session_memory_manifest(exp_id, sess_id)
    return SafeJSONResponse({"experiment_id": exp_id, "session_id": sess_id, "memory_manifest": manifest})


@app.get("/api/experiments/{exp_id}/sessions/{sess_id}/memory/{item_id}")
async def get_experiment_session_memory_item(exp_id: str, sess_id: str, item_id: str):
    session = exp_mgr.get_session(exp_id, sess_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    item = exp_mgr.read_session_memory_item(exp_id, sess_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Memory item not found")
    return SafeJSONResponse(item)


@app.delete("/api/experiments/{exp_id}/sessions/{sess_id}")
async def delete_experiment_session(exp_id: str, sess_id: str):
    if not exp_mgr.delete_session(exp_id, sess_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return JSONResponse({"status": "deleted", "id": sess_id})


@app.post("/api/admin/cleanup")
async def admin_cleanup():
    """Run session and workflow-run cleanup. Uses env: CLEANUP_SESSION_MAX_AGE_DAYS, CLEANUP_SESSION_MAX_PER_EXP, CLEANUP_WORKFLOW_RUNS_KEEP_LAST, CLEANUP_WORKFLOW_RUNS_MAX_AGE_DAYS."""
    max_age = int(os.environ.get("CLEANUP_SESSION_MAX_AGE_DAYS", "0")) or None
    max_per_exp = int(os.environ.get("CLEANUP_SESSION_MAX_PER_EXP", "0")) or None
    wf_keep = int(os.environ.get("CLEANUP_WORKFLOW_RUNS_KEEP_LAST", "20"))
    wf_max_days = int(os.environ.get("CLEANUP_WORKFLOW_RUNS_MAX_AGE_DAYS", "7"))
    session_result = exp_mgr.cleanup_all_old_sessions(max_age_days=max_age, max_sessions_per_experiment=max_per_exp)
    workflow_runs_removed = cleanup_old_workflow_runs(keep_last_n=wf_keep, max_age_days=wf_max_days)
    return JSONResponse({
        "sessions": session_result,
        "workflow_runs_removed": workflow_runs_removed,
    })


@app.get("/api/files/download")
async def download_file(path: str = ""):
    if not path:
        raise HTTPException(status_code=400, detail="path parameter required")
    file_path = Path(path).resolve()
    if not str(file_path).startswith(str(DATA_ROOT.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(file_path), filename=file_path.name, media_type="application/octet-stream")

@app.get("/api/files/serve")
async def serve_file(path: str = ""):
    if not path:
        raise HTTPException(status_code=400, detail="path parameter required")
    file_path = Path(path).resolve()
    if not str(file_path).startswith(str(DATA_ROOT.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        ext = file_path.suffix.lower()
        mime_map = {".csv": "text/csv", ".tsv": "text/tab-separated-values", ".json": "application/json", ".txt": "text/plain", ".log": "text/plain", ".md": "text/markdown", ".html": "text/html", ".htm": "text/html", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp", ".pdf": "application/pdf", ".xpt": "application/octet-stream"}
        mime_type = mime_map.get(ext, "application/octet-stream")
    return FileResponse(path=str(file_path), media_type=mime_type)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
