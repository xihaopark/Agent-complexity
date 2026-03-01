from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path
from typing import Any

from analyzers.dynamic_runtime.analyzer import analyze_dynamic_runs
from analyzers.dynamic_runtime.instrumentor import instrument_python_repo
from analyzers.reporting.generator import generate_report
from analyzers.static_py.analyzer import analyze_python_repo
from analyzers.static_ts.analyzer import analyze_typescript_repo
from analyzers.utils import to_artifact_ref, write_json
from common.events import ArtifactRef, MetricRecord
from common.settings import get_settings
from services.orchestrator.constants import AnalysisStatus
from services.orchestrator.db import session_scope
from services.orchestrator.repository import AnalysisRepository
from services.orchestrator.secrets import get_secret_store
from workers.sandbox_runner.docker_runner import DockerSandboxRunner
from workers.sandbox_runner.git_utils import clone_repository, get_commit_sha
from workers.sandbox_runner.run_spec import detect_run_spec

logger = logging.getLogger(__name__)
settings = get_settings()


def _update_status(analysis_id: str, status: AnalysisStatus, error: str | None = None, obs: float | None = None) -> None:
    with session_scope() as session:
        repo = AnalysisRepository(session)
        job = repo.get_job(analysis_id)
        if job is None:
            return
        repo.update_job_status(job, status=status, error_summary=error, observability_coverage=obs)


def _persist_results(
    analysis_id: str,
    metrics: list[MetricRecord],
    artifacts: list[ArtifactRef],
    composite_score: float | None,
    obs_coverage: float | None,
    final_status: AnalysisStatus,
    error_summary: str | None = None,
) -> None:
    with session_scope() as session:
        repo = AnalysisRepository(session)
        job = repo.get_job(analysis_id)
        if job is None:
            return
        job.artifact_root = str((settings.artifact_root / analysis_id).resolve())
        repo.replace_metrics(analysis_id, metrics)
        repo.replace_artifacts(analysis_id, artifacts)
        if composite_score is not None:
            job.composite_score = composite_score
        if obs_coverage is not None:
            job.observability_coverage = obs_coverage
        repo.update_job_status(job, final_status, error_summary=error_summary)


def _load_job(analysis_id: str) -> dict[str, Any]:
    with session_scope() as session:
        repo = AnalysisRepository(session)
        job = repo.get_job(analysis_id)
        if job is None:
            raise ValueError(f"analysis job {analysis_id} not found")
        return {
            "id": job.id,
            "repo_url": job.repo_url,
            "git_ref": job.git_ref,
            "auth_ref": job.auth_ref,
            "run_spec": job.run_spec or {},
            "run_profile": job.run_profile,
            "repeats": job.repeats,
            "timeout_sec": job.timeout_sec,
        }


def execute_analysis_pipeline(analysis_id: str) -> None:
    _update_status(analysis_id, AnalysisStatus.RUNNING)
    job = _load_job(analysis_id)

    artifact_dir = settings.artifact_root / analysis_id
    workspace_dir = artifact_dir / "workspace"
    repo_dir = workspace_dir / "repo"
    runtime_output_dir = artifact_dir / "runtime"
    static_output_dir = artifact_dir / "static"
    report_output_dir = artifact_dir / "report"

    if workspace_dir.exists():
        shutil.rmtree(workspace_dir, ignore_errors=True)
    workspace_dir.mkdir(parents=True, exist_ok=True)
    runtime_output_dir.mkdir(parents=True, exist_ok=True)
    static_output_dir.mkdir(parents=True, exist_ok=True)
    report_output_dir.mkdir(parents=True, exist_ok=True)

    metrics: list[MetricRecord] = []
    artifacts: list[ArtifactRef] = []

    secret_store = get_secret_store()
    token = secret_store.pop_token(job.get("auth_ref"))

    try:
        clone_repository(job["repo_url"], job["git_ref"], repo_dir, token=token)
    except Exception as exc:
        error = f"clone failed: {type(exc).__name__}: {exc}"
        write_json(artifact_dir / "clone_error.json", {"error": error})
        artifacts.append(to_artifact_ref(artifact_dir / "clone_error.json", "clone_error"))
        _persist_results(
            analysis_id=analysis_id,
            metrics=metrics,
            artifacts=artifacts,
            composite_score=None,
            obs_coverage=0.0,
            final_status=AnalysisStatus.FAILED,
            error_summary=error,
        )
        return

    commit_sha = get_commit_sha(repo_dir)
    run_spec = detect_run_spec(
        repo_path=repo_dir,
        user_spec=job["run_spec"],
        default_repeats=job["repeats"],
        default_timeout_sec=job["timeout_sec"],
    )
    write_json(artifact_dir / "resolved_run_spec.json", run_spec.to_dict())
    artifacts.append(to_artifact_ref(artifact_dir / "resolved_run_spec.json", "resolved_run_spec"))

    try:
        py_metrics, py_artifacts = analyze_python_repo(repo_dir, static_output_dir)
        ts_metrics, ts_artifacts = analyze_typescript_repo(repo_dir, static_output_dir)
        metrics.extend(py_metrics)
        metrics.extend(ts_metrics)
        artifacts.extend(py_artifacts)
        artifacts.extend(ts_artifacts)
        _update_status(analysis_id, AnalysisStatus.STATIC_DONE)
    except Exception as exc:
        error = f"static analysis failed: {type(exc).__name__}: {exc}"
        write_json(artifact_dir / "static_error.json", {"error": error})
        artifacts.append(to_artifact_ref(artifact_dir / "static_error.json", "static_error"))
        _persist_results(
            analysis_id=analysis_id,
            metrics=metrics,
            artifacts=artifacts,
            composite_score=None,
            obs_coverage=0.0,
            final_status=AnalysisStatus.FAILED,
            error_summary=error,
        )
        return

    instrumentation_result = instrument_python_repo(repo_dir)
    write_json(
        artifact_dir / "instrumentation_summary.json",
        {
            "files_total": instrumentation_result.files_total,
            "files_touched": instrumentation_result.files_touched,
            "coverage_of_observability": instrumentation_result.coverage,
        },
    )
    artifacts.append(to_artifact_ref(artifact_dir / "instrumentation_summary.json", "instrumentation_summary"))

    repeats = run_spec.repeats
    timeout_sec = run_spec.timeout_sec
    budget_downgrade = False
    if repeats > 3 and (timeout_sec / max(repeats, 1)) < 120:
        repeats = 3
        budget_downgrade = True
    if budget_downgrade:
        write_json(
            artifact_dir / "budget_adjustment.json",
            {
                "original_repeats": run_spec.repeats,
                "effective_repeats": repeats,
                "reason": "timeout budget too small for N=10",
            },
        )
        artifacts.append(to_artifact_ref(artifact_dir / "budget_adjustment.json", "budget_adjustment"))

    run_results = []
    runner = DockerSandboxRunner()
    dynamic_error: str | None = None
    for idx in range(repeats):
        run_id = f"run_{idx + 1}"
        try:
            result = runner.run(
                repo_path=repo_dir,
                output_path=runtime_output_dir,
                run_id=run_id,
                job_id=analysis_id,
                setup_commands=run_spec.setup_commands,
                entry_command=run_spec.entry_command or "python -V",
                timeout_sec=timeout_sec,
                env_allowlist=run_spec.env_allowlist,
            )
            run_results.append(result)
            artifacts.append(to_artifact_ref(runtime_output_dir / f"stdout_{run_id}.log", "runtime_stdout"))
            artifacts.append(to_artifact_ref(runtime_output_dir / f"stderr_{run_id}.log", "runtime_stderr"))
            if result.event_file.exists():
                artifacts.append(to_artifact_ref(result.event_file, "runtime_events"))
            if result.exit_code != 0 and dynamic_error is None:
                dynamic_error = f"run {run_id} exited with code {result.exit_code}"
                write_json(
                    runtime_output_dir / f"run_exit_{run_id}.json",
                    {"run_id": run_id, "exit_code": result.exit_code, "stderr_tail": result.stderr[-2000:]},
                )
                artifacts.append(to_artifact_ref(runtime_output_dir / f"run_exit_{run_id}.json", "run_exit"))
        except Exception as exc:  # pragma: no cover
            dynamic_error = f"dynamic run failed on {run_id}: {type(exc).__name__}: {exc}"
            write_json(runtime_output_dir / f"dynamic_error_{run_id}.json", {"error": dynamic_error})
            artifacts.append(to_artifact_ref(runtime_output_dir / f"dynamic_error_{run_id}.json", "dynamic_error"))
            break

    obs_coverage = instrumentation_result.coverage
    if run_results:
        event_files = {res.run_id: res.event_file for res in run_results}
        run_stats = {
            res.run_id: {
                "cpu_peak_pct": res.cpu_peak_pct,
                "memory_peak_mb": res.memory_peak_mb,
                "reproducibility_flag": 1.0,
            }
            for res in run_results
        }
        dyn_metrics, dyn_artifacts, dyn_obs = analyze_dynamic_runs(event_files, run_stats, runtime_output_dir)
        metrics.extend(dyn_metrics)
        artifacts.extend(dyn_artifacts)
        obs_coverage = max(obs_coverage, dyn_obs)
        _update_status(analysis_id, AnalysisStatus.DYNAMIC_DONE, obs=obs_coverage)

    merged_events = runtime_output_dir / "events.jsonl"
    with merged_events.open("w", encoding="utf-8") as out:
        for res in run_results:
            if not res.event_file.exists():
                continue
            out.write(res.event_file.read_text(encoding="utf-8", errors="ignore"))
    artifacts.append(to_artifact_ref(merged_events, "events_jsonl"))

    job_meta = {
        "repo_url": job["repo_url"],
        "git_ref": job["git_ref"],
        "commit_sha": commit_sha,
        "run_profile": job["run_profile"],
        "repeats": repeats,
        "timeout_sec": timeout_sec,
        "observability_coverage": obs_coverage,
    }
    write_json(report_output_dir / "job_meta.json", job_meta)
    artifacts.append(to_artifact_ref(report_output_dir / "job_meta.json", "job_meta"))

    composite_enabled = settings.composite_score_enabled
    metrics, report_artifacts = generate_report(
        analysis_id=analysis_id,
        job_meta=job_meta,
        metrics=metrics,
        artifact_dir=report_output_dir,
        composite_enabled=composite_enabled,
    )
    artifacts.extend(report_artifacts)

    composite_score = None
    for metric in metrics:
        if metric.metric_code == "S" and metric.raw_value is not None:
            composite_score = metric.raw_value
            break

    final_status = AnalysisStatus.REPORT_READY
    error_summary = None
    if dynamic_error:
        final_status = AnalysisStatus.PARTIAL
        error_summary = dynamic_error

    _persist_results(
        analysis_id=analysis_id,
        metrics=metrics,
        artifacts=artifacts,
        composite_score=composite_score,
        obs_coverage=obs_coverage,
        final_status=final_status,
        error_summary=error_summary,
    )
