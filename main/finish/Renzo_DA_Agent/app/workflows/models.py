"""Pydantic models for workflow registry and run requests."""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class WorkflowInfo(BaseModel):
    """Metadata for a registered workflow."""

    id: str = Field(..., description="Unique workflow identifier (e.g. '2054', 'metaTAXONx')")
    name: str = Field(..., description="Human-readable workflow name")
    engine: str = Field(..., description="Workflow engine: 'nextflow', 'snakemake', 'r', or 'agent'")
    entry_point: str = Field("", description="Entry file path (e.g. 'main.nf', 'Snakefile'). Empty for agent workflows.")
    path: str = Field(..., description="Absolute path to workflow directory")
    description: Optional[str] = Field(None, description="Workflow description")
    params_schema: Optional[dict[str, Any]] = Field(default_factory=dict, description="Input parameters schema")
    input_hints: Optional[list[str]] = Field(default_factory=list, description="Expected input types (e.g. 'samplesheet', 'fastq')")
    output_hints: Optional[list[str]] = Field(default_factory=list, description="Output descriptions")
    version: Optional[str] = Field(None, description="Workflow version")
    license: Optional[str] = Field(None, description="License identifier")
    url: Optional[str] = Field(None, description="WorkflowHub or source URL")
    aliases: Optional[list[str]] = Field(default_factory=list, description="Alternative workflow identifiers for discovery and CLI entry points")
    tags: Optional[list[str]] = Field(default_factory=list, description="Discovery tags and domain labels")
    discovery: Optional[dict[str, Any]] = Field(default_factory=dict, description="Machine-readable discovery metadata")

    # v2 fields for agent-driven workflows
    know_how: Optional[str] = Field(None, description="Filename of know-how document in workflow dir (e.g. 'SDTM-ADaM.txt')")
    know_how_files: Optional[list[str]] = Field(default_factory=list, description="Ordered list of know-how and skill documents to load for this workflow")
    dataset_dir: Optional[str] = Field(None, description="Relative path to bundled dataset directory (e.g. 'dataset/')")
    default_dataset_ids: Optional[list[str]] = Field(default_factory=list, description="Dataset IDs to auto-link when starting experiment")
    steps: Optional[list[dict[str, Any]]] = Field(default_factory=list, description="Pipeline steps definition")


class WorkflowRunRequest(BaseModel):
    """Request to run a workflow."""

    workflow_id: str = Field(..., description="ID of the workflow to run")
    input_paths: Optional[dict[str, str]] = Field(
        default_factory=dict,
        description="Map of input parameter names to file/directory paths"
    )
    params: Optional[dict[str, Any]] = Field(default_factory=dict, description="Additional workflow parameters")
    profile: Optional[str] = Field("docker", description="Execution profile: 'docker' or 'singularity'")
    session_id: Optional[str] = Field(None, description="Optional session ID for grouping")
    experiment_id: Optional[str] = Field(None, description="Optional experiment ID for workflow-bound sessions")
    execution_mode: Optional[str] = Field(
        None,
        description="Run mode: 'interactive' (stepwise) or 'batch' (background). Defaults: interactive for agent, batch for non-agent.",
    )
    strict_manifest: Optional[bool] = Field(
        True,
        description="If true, enforce manifest step order/dependencies for workflows that provide steps.",
    )
    artifact_policy: Optional[str] = Field(
        "session",
        description="Artifact write policy: 'session', 'shared', or 'dual'.",
    )


class WorkflowRunStatus(BaseModel):
    """Status of a workflow run."""

    run_id: str = Field(..., description="Unique run identifier")
    workflow_id: str = Field(..., description="Workflow that was run")
    status: str = Field(..., description="queued | running | success | failed")
    stdout: Optional[str] = Field(None, description="Standard output")
    stderr: Optional[str] = Field(None, description="Standard error")
    returncode: Optional[int] = Field(None, description="Process return code")
    output_paths: Optional[list[str]] = Field(default_factory=list, description="Paths to output files")
    work_dir: Optional[str] = Field(None, description="Working directory for the run")
    start_ts: Optional[str] = Field(None, description="Start timestamp")
    end_ts: Optional[str] = Field(None, description="End timestamp")
    error: Optional[str] = Field(None, description="Error message if failed")
    error_detail: Optional[dict[str, Any]] = Field(default_factory=dict, description="Structured error details")
