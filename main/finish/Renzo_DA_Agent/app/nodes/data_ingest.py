"""data_ingest node — load and profile data files.

Supports:
  - CSV, Excel, JSON (via pandas)
  - XPT / SAS Transport (via R's haven or pyreadstat)
  - Dataset-JSON (CDISC JSON format)
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
from typing import Dict, List, Optional

import pandas as pd

from renzo.app.state import AgentState

logger = logging.getLogger(__name__)

# CDISC domain detection patterns
_CDISC_DOMAINS = {
    "dm": "Demographics",
    "ae": "Adverse Events",
    "ex": "Exposure",
    "vs": "Vital Signs",
    "lb": "Laboratory",
    "cm": "Concomitant Medications",
    "mh": "Medical History",
    "ds": "Disposition",
    "sv": "Subject Visits",
    "eg": "ECG",
    "pe": "Physical Examination",
    "sc": "Subject Characteristics",
    "su": "Substance Use",
    "ta": "Trial Arms",
    "te": "Trial Elements",
    "ti": "Trial Inclusion/Exclusion",
    "ts": "Trial Summary",
    "tv": "Trial Visits",
}


def _detect_cdisc_domain(file_path: str, columns: List[str]) -> Optional[str]:
    """Detect CDISC domain from filename or column patterns."""
    basename = os.path.splitext(os.path.basename(file_path))[0].lower()

    # Check filename against known domains
    for domain_code, domain_name in _CDISC_DOMAINS.items():
        if basename == domain_code or basename.startswith(domain_code + "_"):
            return domain_name

    # Check for ADaM datasets (ADSL, ADAE, etc.)
    if basename.startswith("ad"):
        return f"ADaM: {basename.upper()}"

    # Check columns for CDISC patterns
    col_upper = {c.upper() for c in columns}
    if "USUBJID" in col_upper and "STUDYID" in col_upper:
        if "DOMAIN" in col_upper:
            return "SDTM (detected from columns)"
        return "CDISC (detected from columns)"

    return None


def _read_xpt_via_r(file_path: str) -> Optional[pd.DataFrame]:
    """Read XPT file using R's haven package (more reliable for CDISC XPT)."""
    if not shutil.which("Rscript"):
        return None

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp_csv = tmp.name

    r_code = f"""
library(haven)
df <- read_xpt("{file_path}")
write.csv(df, "{tmp_csv}", row.names=FALSE)
cat("rows:", nrow(df), "\\n")
cat("cols:", ncol(df), "\\n")
"""
    try:
        result = subprocess.run(
            ["Rscript", "-e", r_code],
            capture_output=True, text=True, check=False, timeout=120
        )
        if result.returncode == 0 and os.path.exists(tmp_csv):
            df = pd.read_csv(tmp_csv)
            os.unlink(tmp_csv)
            return df
    except Exception as e:
        logger.warning("R XPT read failed: %s", e)

    # Clean up
    if os.path.exists(tmp_csv):
        os.unlink(tmp_csv)
    return None


def _read_xpt_via_python(file_path: str) -> Optional[pd.DataFrame]:
    """Read XPT file using pyreadstat (Python fallback)."""
    try:
        import pyreadstat
        df, meta = pyreadstat.read_xport(file_path)
        return df
    except ImportError:
        logger.warning("pyreadstat not available; trying pandas SAS reader")
        try:
            # pandas has basic SAS XPT support
            df = pd.read_sas(file_path, format="xport")
            return df
        except Exception as e:
            logger.warning("pandas SAS reader failed: %s", e)
            return None
    except Exception as e:
        logger.warning("pyreadstat XPT read failed: %s", e)
        return None


def _read_dataset_json(file_path: str) -> Optional[pd.DataFrame]:
    """Read CDISC Dataset-JSON format."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # Dataset-JSON has a specific structure
        # Try standard CDISC Dataset-JSON format
        if "clinicalData" in data or "referenceData" in data:
            # CDISC Dataset-JSON v1.1
            cdata = data.get("clinicalData") or data.get("referenceData", {})
            items = cdata.get("itemGroupData", {})
            if items:
                # Get the first (or only) dataset
                dataset_key = next(iter(items))
                dataset = items[dataset_key]
                columns = [item.get("name", f"col_{i}") for i, item in enumerate(dataset.get("items", []))]
                records = dataset.get("itemData", [])
                df = pd.DataFrame(records, columns=columns)
                return df

        # Try flat JSON (array of records)
        if isinstance(data, list):
            return pd.DataFrame(data)

        # Try records-oriented JSON
        if isinstance(data, dict) and "data" in data:
            return pd.DataFrame(data["data"])

        return pd.DataFrame([data])

    except Exception as e:
        logger.warning("Dataset-JSON read failed: %s", e)
        return None


def _profile_dataframe(df: pd.DataFrame, file_path: str) -> Dict:
    """Create a comprehensive profile of a DataFrame."""
    columns = list(df.columns)
    domain = _detect_cdisc_domain(file_path, columns)

    profile = {
        "file_path": file_path,
        "filename": os.path.basename(file_path),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_count": int(df.shape[1]),
        "row_count": int(df.shape[0]),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing": df.isna().sum().to_dict(),
        "sample": df.head(5).to_dict(orient="list"),
    }

    if domain:
        profile["cdisc_domain"] = domain

    return profile


def _collect_experiment_files(experiment_id: str) -> List[str]:
    """Resolve experiment's linked datasets to a list of absolute file paths."""
    try:
        from renzo.app import datasets as ds_mgr
        from renzo.app import experiments as exp_mgr

        exp_meta = exp_mgr.get_experiment(experiment_id)
        if not exp_meta or not exp_meta.get("dataset_ids"):
            return []

        all_files: List[str] = []
        for ds_id in exp_meta["dataset_ids"]:
            files_dir = ds_mgr.get_dataset_files_dir(ds_id)
            if files_dir and files_dir.is_dir():
                for f in sorted(files_dir.iterdir()):
                    if f.is_file() and not f.name.startswith("."):
                        all_files.append(str(f))
        return all_files
    except Exception as e:
        logger.warning("Failed to resolve experiment datasets: %s", e)
        return []


def _read_file_to_df(file_path: str) -> Optional[pd.DataFrame]:
    """Read a single data file into a DataFrame based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in {".csv"}:
            return pd.read_csv(file_path)
        elif ext in {".xls", ".xlsx"}:
            return pd.read_excel(file_path)
        elif ext in {".xpt"}:
            df = _read_xpt_via_r(file_path)
            if df is None:
                df = _read_xpt_via_python(file_path)
            return df
        elif ext in {".json"}:
            df = _read_dataset_json(file_path)
            if df is None:
                df = pd.read_json(file_path)
            return df
    except Exception as e:
        logger.warning("Failed to read %s: %s", file_path, e)
    return None


def data_ingest_node(state: AgentState) -> Dict:
    """Discover data files and build a lightweight file inventory.

    This is the *discovery* phase. Detailed per-file profiling is delegated
    to the ``data_analyst`` node which runs immediately after.

    Priority:
      1. Experiment-linked datasets (resolved via experiment_id → dataset_ids)
      2. Fallback: files in renzo/data/uploads/

    Supports: CSV, Excel, JSON, XPT (SAS Transport), Dataset-JSON.
    """
    # ── 1. Try experiment-linked datasets first ────────────────────────
    experiment_id = state.get("experiment_id")
    if experiment_id:
        exp_files = _collect_experiment_files(experiment_id)
        if exp_files:
            # Build a lightweight profile with file inventory (no full read)
            primary_path = exp_files[0]
            all_files = []
            for fp in exp_files:
                entry = {"path": fp, "filename": os.path.basename(fp)}
                domain = _detect_cdisc_domain(fp, [])
                if domain:
                    entry["domain"] = domain
                try:
                    entry["size_bytes"] = os.path.getsize(fp)
                except OSError:
                    pass
                all_files.append(entry)

            profile = {
                "file_path": primary_path,
                "filename": os.path.basename(primary_path),
                "all_files": all_files,
            }
            logger.info(
                "Discovered %d experiment dataset files (primary: %s)",
                len(exp_files), os.path.basename(primary_path),
            )
            return {
                "data_profile": profile,
                "data_analyst_mode": "init",
                "next_node": "data_analyst",
                "_data_ingest_attempted": True,
            }

    # ── 2. Fallback: uploads directory ─────────────────────────────────
    uploads_dir = os.path.join(os.getcwd(), "renzo", "data", "uploads")
    if not os.path.isdir(uploads_dir):
        return {"data_profile": {}, "next_node": "planner", "_data_ingest_attempted": True}

    candidates = [f for f in os.listdir(uploads_dir) if not f.startswith(".")]
    if not candidates:
        return {"data_profile": {}, "next_node": "planner", "_data_ingest_attempted": True}

    # Build lightweight inventory for uploads too
    all_files = []
    for fname in candidates:
        fp = os.path.join(uploads_dir, fname)
        entry = {"path": fp, "filename": fname}
        domain = _detect_cdisc_domain(fp, [])
        if domain:
            entry["domain"] = domain
        try:
            entry["size_bytes"] = os.path.getsize(fp)
        except OSError:
            pass
        all_files.append(entry)

    primary_path = all_files[0]["path"] if all_files else ""
    profile = {
        "file_path": primary_path,
        "filename": os.path.basename(primary_path) if primary_path else "",
        "all_files": all_files,
    }
    logger.info("Discovered %d upload file(s) (primary: %s)", len(all_files), os.path.basename(primary_path))
    return {
        "data_profile": profile,
        "data_analyst_mode": "init",
        "next_node": "data_analyst",
        "_data_ingest_attempted": True,
    }
