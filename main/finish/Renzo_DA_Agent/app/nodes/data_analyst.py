"""data_analyst node — maintains a living data catalog throughout the pipeline.

Two operating modes (controlled by ``data_analyst_mode`` in state):

  "init"      — Build the full catalog from experiment-linked datasets.
                Runs after data_ingest, before the planner creates a plan.

  "post_step" — Profile output artifacts from the just-completed step,
                append to catalog with lineage tracking.
                Runs after step_validate (success), before QC.

The catalog is stored in ``state["data_catalog"]`` and is the authoritative
source of data knowledge for the planner, coder, and QC nodes.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import pandas as pd

from renzo.app.state import AgentState
from renzo.app.experiments import resolve_execution_workdir

logger = logging.getLogger(__name__)

# CDISC key columns that commonly serve as join keys
_CDISC_KEY_COLUMNS = {
    "USUBJID", "STUDYID", "SUBJID", "DOMAIN", "VISITNUM", "VISIT",
    "AESEQ", "CMSEQ", "EXSEQ", "LBSEQ", "DSSEQ", "MHSEQ",
}

# CDISC domain detection (shared with data_ingest but kept local to avoid coupling)
_CDISC_DOMAINS = {
    "dm": "Demographics", "ae": "Adverse Events", "ex": "Exposure",
    "vs": "Vital Signs", "lb": "Laboratory", "cm": "Concomitant Medications",
    "mh": "Medical History", "ds": "Disposition", "sv": "Subject Visits",
    "eg": "ECG", "pe": "Physical Examination", "sc": "Subject Characteristics",
    "su": "Substance Use", "ta": "Trial Arms", "te": "Trial Elements",
    "ti": "Trial Inclusion/Exclusion", "ts": "Trial Summary", "tv": "Trial Visits",
    "qs": "Questionnaires", "relrec": "Related Records",
}

_DATA_EXTENSIONS = {".csv", ".xpt", ".json", ".xls", ".xlsx", ".tsv"}


# ── File reading (lightweight — reuses data_ingest readers) ──────────

def _read_file(file_path: str) -> Optional[pd.DataFrame]:
    """Read a data file into a DataFrame. Supports CSV, XPT, JSON, Excel."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".csv":
            return pd.read_csv(file_path)
        elif ext == ".tsv":
            return pd.read_csv(file_path, sep="\t")
        elif ext in {".xls", ".xlsx"}:
            return pd.read_excel(file_path)
        elif ext == ".xpt":
            # Try pyreadstat, fall back to pandas
            try:
                import pyreadstat
                df, _ = pyreadstat.read_xport(file_path)
                return df
            except Exception:
                return pd.read_sas(file_path, format="xport")
        elif ext == ".json":
            return pd.read_json(file_path)
    except Exception as e:
        logger.warning("data_analyst: failed to read %s: %s", file_path, e)
    return None


# ── Profiling ─────────────────────────────────────────────────────────

def _detect_domain(file_path: str) -> str:
    """Detect CDISC domain from filename."""
    basename = os.path.splitext(os.path.basename(file_path))[0].lower()
    for code, name in _CDISC_DOMAINS.items():
        if basename == code or basename.startswith(code + "_"):
            return name
    if basename.startswith("ad"):
        return f"ADaM: {basename.upper()}"
    if basename.startswith("supp"):
        return f"Supplemental: {basename.upper()}"
    return ""


def _detect_key_columns(df: pd.DataFrame) -> List[str]:
    """Identify likely join/key columns."""
    cols_upper = {c.upper(): c for c in df.columns}
    keys = []
    for k in _CDISC_KEY_COLUMNS:
        if k in cols_upper:
            keys.append(cols_upper[k])
    # Also flag any column ending with 'ID' or 'SEQ'
    for c in df.columns:
        cu = c.upper()
        if (cu.endswith("ID") or cu.endswith("SEQ")) and c not in keys:
            keys.append(c)
    return keys


def _compute_value_ranges(df: pd.DataFrame, max_cols: int = 50) -> Dict[str, Any]:
    """Compute value ranges for columns (min/max for numeric, nunique for categorical)."""
    ranges: Dict[str, Any] = {}
    for col in list(df.columns)[:max_cols]:
        try:
            if pd.api.types.is_numeric_dtype(df[col]):
                ranges[col] = {
                    "min": float(df[col].min()) if not df[col].isna().all() else None,
                    "max": float(df[col].max()) if not df[col].isna().all() else None,
                }
            else:
                nunique = int(df[col].nunique())
                info: Dict[str, Any] = {"unique": nunique}
                if nunique <= 20:
                    info["values"] = df[col].dropna().unique().tolist()[:20]
                ranges[col] = info
        except Exception:
            continue
    return ranges


def _profile_file_detailed(
    file_path: str,
    source: str = "input",
    dataset_id: Optional[str] = None,
    step_id: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Create a detailed catalog entry for a single data file."""
    df = _read_file(file_path)
    if df is None:
        return None

    n_rows = int(df.shape[0])
    n_cols = int(df.shape[1])
    col_names = list(df.columns)
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    # Missing percentage per column
    missing_pct: Dict[str, float] = {}
    if n_rows > 0:
        missing_pct = {col: round(float(df[col].isna().mean()) * 100, 1) for col in col_names}

    # Sample rows (first 3)
    sample_rows: List[Dict] = []
    try:
        for _, row in df.head(3).iterrows():
            sample_rows.append({k: _safe_val(v) for k, v in row.items()})
    except Exception:
        pass

    key_columns = _detect_key_columns(df)
    value_ranges = _compute_value_ranges(df)
    domain = _detect_domain(file_path)

    entry: Dict[str, Any] = {
        "file_path": file_path,
        "filename": os.path.basename(file_path),
        "source": source,
        "dataset_id": dataset_id,
        "step_id": step_id,
        "domain": domain,
        "rows": n_rows,
        "columns": n_cols,
        "column_names": col_names,
        "dtypes": dtypes,
        "missing_pct": missing_pct,
        "sample_rows": sample_rows,
        "key_columns": key_columns,
        "value_ranges": value_ranges,
        "profiled_at": datetime.now(timezone.utc).isoformat(),
    }
    return entry


def _safe_val(v: Any) -> Any:
    """Make a value JSON-safe."""
    if pd.isna(v):
        return None
    if isinstance(v, (int, float, str, bool)):
        return v
    return str(v)


# ── Catalog summary for LLM prompts ──────────────────────────────────

def build_catalog_summary(
    catalog: List[Dict[str, Any]],
    step_context: str = "",
    max_files: int = 30,
    include_samples: bool = False,
) -> str:
    """Generate a concise text summary of the data catalog for LLM prompts.

    Parameters
    ----------
    catalog : list of catalog entries
    step_context : optional description of the current step (for relevance hints)
    max_files : max files to include
    include_samples : whether to include sample rows
    """
    if not catalog:
        return ""

    # Group by source
    inputs = [e for e in catalog if e.get("source") == "input"]
    intermediates = [e for e in catalog if e.get("source") == "intermediate"]
    outputs = [e for e in catalog if e.get("source") == "output"]

    lines = ["=== DATA CATALOG ==="]

    def _fmt_file(entry: Dict, idx: int) -> List[str]:
        flines = []
        domain_str = f" [{entry.get('domain', '')}]" if entry.get("domain") else ""
        flines.append(
            f"  {idx}. {entry['filename']}{domain_str} — "
            f"{entry['rows']} rows x {entry['columns']} cols"
        )
        flines.append(f"     Path: {entry['file_path']}")
        flines.append(f"     Columns: {', '.join(entry.get('column_names', [])[:30])}")
        keys = entry.get("key_columns", [])
        if keys:
            flines.append(f"     Key columns: {', '.join(keys)}")
        # Show columns with high missing %
        bad_missing = {c: v for c, v in entry.get("missing_pct", {}).items() if v > 10}
        if bad_missing:
            top = sorted(bad_missing.items(), key=lambda x: -x[1])[:5]
            flines.append(f"     High missing: {', '.join(f'{c}({v}%)' for c, v in top)}")
        if include_samples and entry.get("sample_rows"):
            flines.append(f"     Sample: {entry['sample_rows'][0]}")
        return flines

    if inputs:
        lines.append(f"\nInput datasets ({len(inputs)} files):")
        for i, e in enumerate(inputs[:max_files], 1):
            lines.extend(_fmt_file(e, i))

    if intermediates:
        lines.append(f"\nIntermediate outputs ({len(intermediates)} files):")
        for i, e in enumerate(intermediates[:max_files], 1):
            lines.extend(_fmt_file(e, i))

    if outputs:
        lines.append(f"\nStep outputs ({len(outputs)} files):")
        for i, e in enumerate(outputs[:max_files], 1):
            lines.extend(_fmt_file(e, i))

    # Cross-file key analysis
    all_keys: Dict[str, int] = {}
    for e in catalog:
        for k in e.get("key_columns", []):
            ku = k.upper()
            all_keys[ku] = all_keys.get(ku, 0) + 1
    shared_keys = {k: v for k, v in all_keys.items() if v > 1}
    if shared_keys:
        lines.append(f"\nShared join keys across files:")
        for k, cnt in sorted(shared_keys.items(), key=lambda x: -x[1]):
            lines.append(f"  - {k} (in {cnt} files)")

    lines.append("=== END DATA CATALOG ===")
    return "\n".join(lines)


# ── Post-step output profiling ────────────────────────────────────────

def _profile_step_outputs(
    outputs_dir: str,
    step_id: str,
    existing_paths: set,
) -> List[Dict[str, Any]]:
    """Scan output directory for new data files and profile them."""
    new_entries: List[Dict[str, Any]] = []
    if not os.path.isdir(outputs_dir):
        return new_entries

    for fname in sorted(os.listdir(outputs_dir)):
        fpath = os.path.join(outputs_dir, fname)
        if not os.path.isfile(fpath):
            continue
        if fpath in existing_paths:
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext not in _DATA_EXTENSIONS:
            continue
        entry = _profile_file_detailed(fpath, source="output", step_id=step_id)
        if entry:
            new_entries.append(entry)

    return new_entries


# ── Main node function ────────────────────────────────────────────────

def data_analyst_node(state: AgentState) -> Dict:
    """Data analyst node — builds and maintains the data catalog.

    Mode is determined by ``state["data_analyst_mode"]``:

      "init"      — Full catalog build from experiment datasets + data_profile.
      "post_step" — Profile outputs from the just-completed step.
    """
    mode = state.get("data_analyst_mode", "init")
    catalog = list(state.get("data_catalog", []))
    lineage = list(state.get("data_lineage", []))

    if mode == "init":
        return _run_init_mode(state, catalog, lineage)
    elif mode == "post_step":
        return _run_post_step_mode(state, catalog, lineage)
    else:
        logger.warning("data_analyst: unknown mode '%s', treating as init", mode)
        return _run_init_mode(state, catalog, lineage)


def _run_init_mode(state: AgentState, catalog: List, lineage: List) -> Dict:
    """Build full catalog from experiment-linked datasets."""
    # Collect file paths from experiment datasets
    experiment_id = state.get("experiment_id")
    file_paths: List[str] = []
    ds_id_map: Dict[str, str] = {}  # file_path -> dataset_id

    if experiment_id:
        try:
            from renzo.app import datasets as ds_mgr
            from renzo.app import experiments as exp_mgr

            exp_meta = exp_mgr.get_experiment(experiment_id)
            if exp_meta and exp_meta.get("dataset_ids"):
                for ds_id in exp_meta["dataset_ids"]:
                    files_dir = ds_mgr.get_dataset_files_dir(ds_id)
                    if files_dir and files_dir.is_dir():
                        for f in sorted(files_dir.iterdir()):
                            if f.is_file() and not f.name.startswith("."):
                                ext = f.suffix.lower()
                                if ext in _DATA_EXTENSIONS:
                                    fp = str(f)
                                    file_paths.append(fp)
                                    ds_id_map[fp] = ds_id
        except Exception as e:
            logger.warning("data_analyst init: failed to resolve datasets: %s", e)

    # Also include the primary file from data_profile if not already covered
    data_profile = state.get("data_profile", {})
    primary_path = data_profile.get("file_path", "")
    if primary_path and primary_path not in file_paths:
        file_paths.insert(0, primary_path)

    # Also check data_profile.all_files
    for af in data_profile.get("all_files", []):
        fp = af.get("path", "")
        if fp and fp not in file_paths:
            file_paths.append(fp)

    # Profile each file
    existing_paths = {e["file_path"] for e in catalog}
    new_count = 0
    for fp in file_paths:
        if fp in existing_paths:
            continue
        entry = _profile_file_detailed(fp, source="input", dataset_id=ds_id_map.get(fp))
        if entry:
            catalog.append(entry)
            new_count += 1

    logger.info(
        "data_analyst init: profiled %d new files (catalog total: %d)",
        new_count, len(catalog),
    )

    # Also update the legacy data_profile with richer info from catalog
    # so existing planner/coder code still works
    updated_profile = dict(data_profile)
    if catalog and not updated_profile.get("file_path"):
        first = catalog[0]
        updated_profile["file_path"] = first["file_path"]
        updated_profile["filename"] = first["filename"]
        updated_profile["rows"] = first["rows"]
        updated_profile["columns"] = first["columns"]
        updated_profile["dtypes"] = first["dtypes"]
        updated_profile["missing"] = {
            c: int(first["rows"] * v / 100)
            for c, v in first.get("missing_pct", {}).items()
        }
        updated_profile["sample"] = {}
        if first.get("sample_rows"):
            # Convert list-of-dicts to dict-of-lists for backward compat
            for key in first["sample_rows"][0]:
                updated_profile["sample"][key] = [r.get(key) for r in first["sample_rows"]]

    # Build all_files list for backward compat
    updated_profile["all_files"] = [
        {
            "path": e["file_path"],
            "filename": e["filename"],
            "domain": e.get("domain", ""),
            "size_bytes": os.path.getsize(e["file_path"]) if os.path.exists(e["file_path"]) else 0,
        }
        for e in catalog if e.get("source") == "input"
    ]

    return {
        "data_catalog": catalog,
        "data_lineage": lineage,
        "data_profile": updated_profile,
        "data_analyst_mode": "",
        "next_node": "planner",
    }


def _run_post_step_mode(state: AgentState, catalog: List, lineage: List) -> Dict:
    """Profile outputs from the just-completed step."""
    current_step_id = state.get("current_step_id", "unknown")

    # Determine output directories to scan
    scan_dirs: List[str] = []
    experiment_id = state.get("experiment_id")
    session_id = state.get("session_id")
    base = os.getcwd()

    execution_workdir = state.get("execution_workdir")
    artifact_policy = state.get("artifact_policy", "session")
    if execution_workdir:
        scan_dirs.append(execution_workdir)
    else:
        scan_dirs.append(str(resolve_execution_workdir(experiment_id, session_id, artifact_policy)))
        if experiment_id and session_id:
            scan_dirs.append(os.path.join(base, "renzo", "data", "experiments", experiment_id, "sessions", session_id, "output"))
        if experiment_id:
            scan_dirs.append(os.path.join(base, "renzo", "data", "experiments", experiment_id, "output"))
    # Compatibility read of legacy shared path (opt-in)
    if artifact_policy in {"shared", "dual"}:
        scan_dirs.append(os.path.join(base, "renzo", "data", "artifacts"))

    existing_paths = {e["file_path"] for e in catalog}
    new_entries: List[Dict] = []
    for d in scan_dirs:
        new_entries.extend(_profile_step_outputs(d, current_step_id, existing_paths))
        # Update existing_paths to avoid double-counting
        existing_paths.update(e["file_path"] for e in new_entries)

    catalog.extend(new_entries)

    # Record lineage
    if new_entries:
        lineage.append({
            "step_id": current_step_id,
            "inputs": [e["file_path"] for e in catalog if e.get("source") == "input"],
            "outputs": [e["file_path"] for e in new_entries],
            "transform": f"Step {current_step_id} produced {len(new_entries)} output file(s)",
        })

    logger.info(
        "data_analyst post_step: profiled %d new output files for step %s",
        len(new_entries), current_step_id,
    )

    return {
        "data_catalog": catalog,
        "data_lineage": lineage,
        "data_analyst_mode": "",
        "next_node": "qc",
    }
