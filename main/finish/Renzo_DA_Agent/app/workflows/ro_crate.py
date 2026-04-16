"""RO-Crate metadata parser for WorkflowHub workflow crates."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from renzo.app.workflows.models import WorkflowInfo


def _get_by_id(graph: list[dict], entity_id: str) -> Optional[dict]:
    """Find entity in @graph by @id."""
    for node in graph:
        if node.get("@id") == entity_id:
            return node
    return None


def _infer_engine(entry_point: str, programming_language: Any) -> str:
    """Infer workflow engine from entry point filename or programmingLanguage."""
    if programming_language:
        lang_id = programming_language.get("@id", "") if isinstance(programming_language, dict) else str(programming_language)
        if "nextflow" in lang_id.lower():
            return "nextflow"
        if "snakemake" in lang_id.lower():
            return "snakemake"
    ep = entry_point.lower()
    if ep.endswith(".nf") or ep == "main.nf":
        return "nextflow"
    if "snakefile" in ep or ep.endswith(".smk"):
        return "snakemake"
    return "nextflow"  # default


def parse_ro_crate(workflow_dir: Path) -> Optional[WorkflowInfo]:
    """
    Parse ro-crate-metadata.json and build WorkflowInfo.
    Returns None if not a valid workflow RO-Crate (e.g. no mainEntity or unsupported engine).
    """
    meta_path = workflow_dir / "ro-crate-metadata.json"
    if not meta_path.exists():
        return None

    try:
        with open(meta_path, encoding="utf-8") as f:
            crate = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    graph = crate.get("@graph", [])
    if not graph:
        return None

    # Root dataset is usually "./" or has mainEntity
    root = _get_by_id(graph, "./") or _get_by_id(graph, "ro-crate-metadata.json")
    if not root:
        # Try first CreativeWork/Dataset
        for node in graph:
            if "Dataset" in node.get("@type", []) or "CreativeWork" in node.get("@type", []):
                root = node
                break
    if not root:
        return None

    main_entity_ref = root.get("mainEntity")
    if not main_entity_ref:
        return None

    entity_id = main_entity_ref.get("@id") if isinstance(main_entity_ref, dict) else main_entity_ref
    if not entity_id:
        return None

    main_entity = _get_by_id(graph, entity_id)
    if not main_entity:
        return None

    # Entry point: main.nf, Snakefile, etc.
    entry_point = entity_id
    if entry_point.startswith("./"):
        entry_point = entry_point[2:]
    if "/" in entry_point:
        entry_point = entry_point.split("/")[-1]

    programming_language = main_entity.get("programmingLanguage")
    engine = _infer_engine(entry_point, programming_language)

    # Only support Nextflow and Snakemake for now
    if engine not in ("nextflow", "snakemake"):
        return None

    # Workflow ID: use identifier from root, or directory name
    identifier = root.get("identifier", "")
    if isinstance(identifier, str) and "workflowhub" in identifier.lower():
        # Extract workflow ID from URL like https://workflowhub.eu/workflows/2054?version=1
        import re
        m = re.search(r"workflows/(\d+)", identifier)
        wf_id = m.group(1) if m else workflow_dir.name
    else:
        wf_id = workflow_dir.name

    name = main_entity.get("name") or root.get("name") or workflow_dir.name
    if isinstance(name, list):
        name = name[0] if name else workflow_dir.name

    description = main_entity.get("description") or root.get("description")
    if isinstance(description, str) and len(description) > 500:
        description = description[:500] + "..."

    version = main_entity.get("version") or root.get("version")
    if version is not None:
        version = str(version)

    license_val = main_entity.get("license") or root.get("license")
    if isinstance(license_val, dict):
        license_val = license_val.get("@id") or license_val.get("name")
    license_str = str(license_val) if license_val else None

    url = main_entity.get("url") or root.get("url")
    if isinstance(url, dict):
        url = url.get("@id")
    url_str = str(url) if url else None

    # Input/output from main entity
    input_spec = main_entity.get("input", [])
    output_spec = main_entity.get("output", [])
    input_hints = []
    output_hints = []
    if isinstance(input_spec, list):
        for inp in input_spec:
            if isinstance(inp, dict):
                input_hints.append(inp.get("name", inp.get("@id", "input")))
            else:
                input_hints.append(str(inp))
    if isinstance(output_spec, list):
        for out in output_spec:
            if isinstance(out, dict):
                output_hints.append(out.get("name", out.get("@id", "output")))
            else:
                output_hints.append(str(out))

    params_schema = {}
    # Could extend with FormalParameter extraction from CWL/WfExS; for now minimal

    return WorkflowInfo(
        id=wf_id,
        name=name,
        engine=engine,
        entry_point=entry_point,
        path=str(workflow_dir.resolve()),
        description=description,
        params_schema=params_schema,
        input_hints=input_hints if input_hints else ["input", "samplesheet"],
        output_hints=output_hints,
        version=version,
        license=license_str,
        url=url_str,
    )
