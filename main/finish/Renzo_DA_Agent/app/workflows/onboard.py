"""Workflow onboarding: acquire from GitHub/zip/folder, understand, write to workflow_pool."""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Dict, Optional

from renzo.app.workflows.registry import discover_workflows, get_workflow_by_id
from renzo.app.workflows.ro_crate import parse_ro_crate
from renzo.app.workflows.models import WorkflowInfo

logger = logging.getLogger(__name__)

# Default pool path (same as wf_manager)
def _default_pool_path() -> Path:
    env_path = os.environ.get("WORKFLOW_POOL_DIR")
    if env_path:
        return Path(env_path).resolve()
    base = Path(__file__).resolve().parent.parent.parent
    return (base / "workflow_pool").resolve()


def _github_url_to_id(url: str) -> str:
    """Extract a stable workflow id from GitHub URL, e.g. nf-core/proteinfamilies -> proteinfamilies."""
    url = (url or "").strip().rstrip("/")
    if ".git" in url:
        url = url.replace(".git", "")
    parts = url.replace("https://github.com/", "").replace("http://github.com/", "").replace("git@github.com:", "").strip("/").split("/")
    if not parts:
        return "workflow"
    last = parts[-1]
    return re.sub(r"[^a-zA-Z0-9_-]", "-", last).strip("-") or "workflow"


def _acquire_from_github(url: str, branch: str = "main") -> Path:
    """Clone repo to a temp dir. Returns path to workflow root (clone root)."""
    url = url.strip().rstrip("/")
    if not url or "github.com" not in url:
        raise ValueError("Invalid GitHub URL")
    branch = branch or "main"
    staging = Path(tempfile.mkdtemp(prefix="renzo_import_"))
    try:
        cmd = ["git", "clone", "--depth", "1", "--branch", branch, url, str(staging)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            raise RuntimeError(f"git clone failed: {r.stderr or r.stdout}")
        return staging
    except subprocess.TimeoutExpired:
        shutil.rmtree(staging, ignore_errors=True)
        raise RuntimeError("git clone timed out")
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def _acquire_from_zip(zip_path: str) -> tuple[Path, Path]:
    """Unzip to temp dir. Returns (workflow_root, staging_root_for_cleanup)."""
    p = Path(zip_path)
    if not p.is_file() or p.suffix.lower() != ".zip":
        raise ValueError("Invalid zip path or file not found")
    staging = Path(tempfile.mkdtemp(prefix="renzo_import_"))
    with zipfile.ZipFile(p, "r") as zf:
        zf.extractall(staging)
    # Prefer single top-level dir that looks like workflow root
    entries = [x for x in staging.iterdir()]
    if len(entries) == 1 and entries[0].is_dir():
        candidate = entries[0]
        if (candidate / "ro-crate-metadata.json").exists() or (candidate / "main.nf").exists() or (candidate / "Snakefile").exists():
            return candidate, staging
    if (staging / "ro-crate-metadata.json").exists() or (staging / "main.nf").exists() or (staging / "Snakefile").exists():
        return staging, staging
    return staging, staging


def _acquire_from_folder(folder_path: str) -> Path:
    """Use server path as workflow root (no copy yet)."""
    p = Path(folder_path).resolve()
    if not p.is_dir():
        raise ValueError("Folder path is not a directory")
    return p


def _understand(workflow_root: Path) -> tuple[Optional[WorkflowInfo], Optional[Dict[str, Any]]]:
    """
    Parse workflow_root. Returns (WorkflowInfo if RO-Crate, else None; heuristic_summary if no RO-Crate).
    WorkflowInfo.path may point to staging; caller will copy to pool.
    """
    meta = workflow_root / "ro-crate-metadata.json"
    if meta.exists():
        info = parse_ro_crate(workflow_root)
        if info:
            return info, None
    # Heuristic: look for main.nf or Snakefile
    engine = None
    entry_point = ""
    for f in workflow_root.iterdir():
        if not f.is_file():
            continue
        name = f.name
        if name == "main.nf" or (name.endswith(".nf") and not entry_point):
            engine = "nextflow"
            entry_point = name
            break
        if name == "Snakefile" or name.endswith(".smk"):
            engine = "snakemake"
            entry_point = name
            break
    if not engine:
        return None, None
    # Name/description from README
    name = workflow_root.name
    description = ""
    for readme in ("README.md", "README.rst", "README"):
        rp = workflow_root / readme
        if rp.is_file():
            try:
                text = rp.read_text(encoding="utf-8", errors="ignore")[:2000]
                first = text.split("\n\n")[0].strip()
                if first.startswith("#"):
                    name = first.lstrip("#").strip().split("\n")[0]
                description = first[:500] if first else ""
            except Exception:
                pass
            break
    suggested_id = re.sub(r"[^a-zA-Z0-9_-]", "-", workflow_root.name).strip("-") or "workflow"
    summary = {
        "engine": engine,
        "entry_point": entry_point,
        "name": name,
        "description": description,
        "suggested_id": suggested_id,
        "path": str(workflow_root.resolve()),
    }
    return None, summary


def _decide_final_id(
    suggested_id: Optional[str],
    id_hint_from_github: Optional[str],
    from_ro_crate: Optional[WorkflowInfo],
    from_heuristic: Optional[Dict[str, Any]],
    pool_path: Path,
) -> str:
    if suggested_id:
        final = re.sub(r"[^a-zA-Z0-9_-]", "-", suggested_id.strip()).strip("-")
        if not final:
            final = id_hint_from_github or (from_ro_crate.id if from_ro_crate else (from_heuristic or {}).get("suggested_id", "workflow"))
    elif id_hint_from_github:
        final = id_hint_from_github
    elif from_ro_crate:
        final = from_ro_crate.id
    elif from_heuristic:
        final = from_heuristic.get("suggested_id", "workflow")
    else:
        raise ValueError("Could not determine workflow id")
    existing = {w.id for w in discover_workflows(pool_path)}
    if final in existing:
        raise ValueError(f"Workflow ID already exists: {final}")
    return final


def _know_how_content(engine: str, entry_point: str, name: str, url: Optional[str] = None) -> str:
    url_line = f"\n- Source: {url}" if url else ""
    return f"""# {name} — Know-how (auto-generated)

- **Engine**: {engine}
- **Entry**: {entry_point}
- **Input**: See README; typically `--input` (samplesheet) and `--outdir` for Nextflow.
- **Profile**: Use `-profile docker` or `-profile singularity` or `-profile test` for test data.
{url_line}
"""


def _write(
    workflow_root: Path,
    final_id: str,
    from_ro_crate: Optional[WorkflowInfo],
    from_heuristic: Optional[Dict[str, Any]],
    pool_path: Path,
    update_gitignore: bool = True,
) -> None:
    pool_path = pool_path.resolve()
    workflow_root = workflow_root.resolve()
    dest = pool_path / final_id
    if dest.exists():
        raise RuntimeError(f"Target directory already exists: {dest}")
    shutil.copytree(workflow_root, dest, symlinks=False)
    name = (from_ro_crate.name if from_ro_crate else (from_heuristic or {}).get("name", final_id))
    engine = (from_ro_crate.engine if from_ro_crate else (from_heuristic or {}).get("engine", "nextflow"))
    entry_point = (from_ro_crate.entry_point if from_ro_crate else (from_heuristic or {}).get("entry_point", "main.nf"))
    url = from_ro_crate.url if from_ro_crate else None
    know_how_body = _know_how_content(engine, entry_point, name, url)
    (dest / "know-how.md").write_text(know_how_body, encoding="utf-8")
    if from_ro_crate:
        sidecar = {
            "know_how": "know-how.md",
            "default_dataset_ids": [],
        }
        (dest / "manifest.json").write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    else:
        manifest = {
            "id": final_id,
            "name": name,
            "engine": engine,
            "entry_point": entry_point,
            "description": (from_heuristic or {}).get("description", ""),
            "input_hints": ["input", "samplesheet"],
            "output_hints": [],
            "know_how": "know-how.md",
            "default_dataset_ids": [],
        }
        (dest / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    if update_gitignore:
        gitignore_path = pool_path.parent / ".gitignore"
        if gitignore_path.is_file():
            line = f"workflow_pool/{final_id}/\n"
            content = gitignore_path.read_text(encoding="utf-8")
            if line.strip() not in content and f"workflow_pool/{final_id}" not in content:
                gitignore_path.write_text(content.rstrip() + "\n" + line, encoding="utf-8")


def _validate(final_id: str, pool_path: Path) -> Dict[str, Any]:
    wf = get_workflow_by_id(final_id, pool_path)
    if not wf:
        raise RuntimeError(f"Workflow not discovered after import: {final_id}")
    return {"workflow_id": wf.id, "name": wf.name, "engine": wf.engine}


def _run_pipeline(
    workflow_root: Path,
    suggested_id: Optional[str],
    pool_path: Path,
    update_gitignore: bool,
    cleanup_staging: Optional[Path] = None,
    id_hint_from_github: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        pool_path = pool_path.resolve()
        from_ro_crate, from_heuristic = _understand(workflow_root)
        if from_ro_crate is None and from_heuristic is None:
            raise ValueError("No supported workflow found (no RO-Crate and no main.nf/Snakefile)")
        final_id = _decide_final_id(suggested_id, id_hint_from_github, from_ro_crate, from_heuristic, pool_path)
        _write(workflow_root, final_id, from_ro_crate, from_heuristic, pool_path, update_gitignore=update_gitignore)
        result = _validate(final_id, pool_path)
        return result
    finally:
        if cleanup_staging and cleanup_staging.exists():
            shutil.rmtree(cleanup_staging, ignore_errors=True)


def import_workflow_from_github(
    url: str,
    branch: str = "main",
    suggested_id: Optional[str] = None,
    pool_path: Optional[Path] = None,
    update_gitignore: bool = True,
) -> Dict[str, Any]:
    """Clone from GitHub, then acquire -> understand -> decide -> write -> validate."""
    pool = (pool_path or _default_pool_path()).resolve()
    pool.mkdir(parents=True, exist_ok=True)
    staging = _acquire_from_github(url, branch)
    id_from_url = _github_url_to_id(url)
    try:
        return _run_pipeline(
            staging,
            suggested_id,
            pool,
            update_gitignore,
            cleanup_staging=staging,
            id_hint_from_github=id_from_url if not suggested_id else None,
        )
    except Exception as e:
        shutil.rmtree(staging, ignore_errors=True)
        raise RuntimeError(str(e)) from e


def import_workflow_from_zip(
    zip_path: str,
    suggested_id: Optional[str] = None,
    pool_path: Optional[Path] = None,
    update_gitignore: bool = True,
) -> Dict[str, Any]:
    """Unzip, then run pipeline. Caller may delete zip_path after return."""
    pool = pool_path or _default_pool_path()
    pool.mkdir(parents=True, exist_ok=True)
    workflow_root, staging_root = _acquire_from_zip(zip_path)
    try:
        return _run_pipeline(workflow_root, suggested_id, pool, update_gitignore, cleanup_staging=staging_root)
    except Exception as e:
        shutil.rmtree(staging_root, ignore_errors=True)
        raise RuntimeError(str(e)) from e


def import_workflow_from_folder(
    folder_path: str,
    suggested_id: Optional[str] = None,
    pool_path: Optional[Path] = None,
    update_gitignore: bool = True,
) -> Dict[str, Any]:
    """Copy folder into pool, then run pipeline. Original folder is not modified."""
    pool = pool_path or _default_pool_path()
    pool.mkdir(parents=True, exist_ok=True)
    workflow_root = _acquire_from_folder(folder_path)
    return _run_pipeline(workflow_root, suggested_id, pool, update_gitignore, cleanup_staging=None)
