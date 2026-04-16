"""Pre-built code snippets for common data operations.

Instead of asking the LLM to regenerate "read a CSV" or "profile a dataframe"
every single time, the coder node injects these tested, working snippets into
the LLM prompt or uses them as direct building blocks.

Design principles:
  - Each snippet is a standalone, executable block
  - Python by default for data I/O and profiling (faster, more reliable)
  - R only when pharmaverse-specific packages are actually needed
  - Snippets are parameterized with {placeholders}
"""
from __future__ import annotations

import os
from typing import Dict, List, Optional


# ── Python snippets ─────────────────────────────────────────────────────

PYTHON_READ_CSV = '''\
import pandas as pd
import os

df = pd.read_csv("{file_path}")
print(f"Loaded {os.path.basename('{file_path}')}: {{df.shape[0]}} rows x {{df.shape[1]}} cols")
'''

PYTHON_READ_MULTI_CSV = '''\
import pandas as pd
import os

data_dir = "{data_dir}"
datasets = {{}}
for fname in sorted(os.listdir(data_dir)):
    if fname.endswith(".csv") and not fname.startswith("."):
        fpath = os.path.join(data_dir, fname)
        name = os.path.splitext(fname)[0].lower()
        datasets[name] = pd.read_csv(fpath)
        print(f"  {{name}}: {{datasets[name].shape[0]}} rows x {{datasets[name].shape[1]}} cols")
print(f"\\nLoaded {{len(datasets)}} dataset(s) from {{data_dir}}")
'''

PYTHON_PROFILE_DF = '''\
def profile_df(df, name="dataset"):
    """Quick profile of a DataFrame."""
    print(f"\\n=== {name} ===")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} cols")
    print(f"Columns: {', '.join(df.columns[:20])}")
    print(f"Dtypes: {dict(df.dtypes.value_counts())}")
    missing = df.isna().sum()
    if missing.any():
        print(f"Missing: {dict(missing[missing > 0])}")
    print(df.head(3).to_string())
    return df
'''

PYTHON_SAVE_CSV = '''\
{df_name}.to_csv("{output_name}", index=False)
print(f"Saved {output_name}: {{{df_name}.shape[0]}} rows x {{{df_name}.shape[1]}} cols")
'''

PYTHON_COMPARE_SCHEMAS = '''\
def compare_schemas(derived_df, truth_df, name="dataset"):
    """Compare a derived dataset against ground truth."""
    d_cols = set(derived_df.columns)
    t_cols = set(truth_df.columns)
    missing = t_cols - d_cols
    extra = d_cols - t_cols
    common = d_cols & t_cols
    print(f"\\n=== Schema comparison: {name} ===")
    print(f"  Derived: {len(d_cols)} cols, Truth: {len(t_cols)} cols, Common: {len(common)}")
    if missing:
        print(f"  Missing from derived: {missing}")
    if extra:
        print(f"  Extra in derived: {extra}")
    # Row count comparison
    print(f"  Rows - derived: {derived_df.shape[0]}, truth: {truth_df.shape[0]}")
    return {"missing": missing, "extra": extra, "common": common}
'''


# ── R snippets ──────────────────────────────────────────────────────────

R_READ_CSV = '''\
#!R
library(readr)
{var_name} <- read_csv("{file_path}", show_col_types = FALSE)
cat("{var_name}:", nrow({var_name}), "rows x", ncol({var_name}), "cols\\n")
'''

R_READ_MULTI_CSV = '''\
#!R
library(readr)
library(purrr)

data_dir <- "{data_dir}"
csv_files <- list.files(data_dir, pattern = "\\\\.csv$", full.names = TRUE)
datasets <- set_names(csv_files, tools::file_path_sans_ext(basename(csv_files))) |>
  map(\\(f) read_csv(f, show_col_types = FALSE))
walk2(names(datasets), datasets, \\(n, d) cat(n, ":", nrow(d), "rows x", ncol(d), "cols\\n"))
'''

R_ADMIRAL_ADSL = '''\
#!R
suppressPackageStartupMessages({{
  library(admiral)
  library(dplyr)
  library(readr)
  library(lubridate)
  library(stringr)
}})

sdtm_dir <- "{sdtm_dir}"
dm <- read_csv(file.path(sdtm_dir, "dm.csv"), show_col_types = FALSE)
'''

R_SAVE_XPT = '''\
library(haven)
write_xpt({df_name}, "{output_name}")
cat("Saved {output_name}:", nrow({df_name}), "rows x", ncol({df_name}), "cols\\n")
'''


# ── Snippet registry ────────────────────────────────────────────────────

# Maps operation type -> (language, snippet template)
SNIPPET_REGISTRY: Dict[str, Dict[str, str]] = {
    "read_csv": {
        "python": PYTHON_READ_CSV,
        "r": R_READ_CSV,
    },
    "read_multi_csv": {
        "python": PYTHON_READ_MULTI_CSV,
        "r": R_READ_MULTI_CSV,
    },
    "profile": {
        "python": PYTHON_PROFILE_DF,
    },
    "save_csv": {
        "python": PYTHON_SAVE_CSV,
    },
    "compare_schemas": {
        "python": PYTHON_COMPARE_SCHEMAS,
    },
    "admiral_adsl": {
        "r": R_ADMIRAL_ADSL,
    },
    "save_xpt": {
        "r": R_SAVE_XPT,
    },
}


# ── Step-type to language mapping ───────────────────────────────────────

# Operations that genuinely require R (pharmaverse packages).
# NOTE: Keep this list narrow — only pharmaverse-specific tools that
# have no Python equivalent. Generic ADaM/SDTM data manipulation
# (reading CSV, merging, filtering) should default to Python/pandas.
_R_REQUIRED_KEYWORDS = {
    "admiral", "derive_var", "derive_vars", "derive_param",
    "xportr", "write_xpt", "read_xpt",
    "metacore", "metatools",
    "rtables", "gtsummary", "tplyr",
}

# Operations where Python is better
_PYTHON_PREFERRED_KEYWORDS = {
    "profile", "profiling", "read data", "load data", "inspect",
    "summary statistics", "data exploration", "data quality",
    "schema comparison", "compare", "validation report",
    "qc report", "conformance check", "specification design",
    "merge", "join", "concatenate", "missing values",
    "visualization", "plot", "chart", "histogram",
}


def select_language_for_step(step_description: str, step_type: str = "") -> str:
    """Choose the best language for a step.

    Returns "python" or "r". Defaults to Python unless the step genuinely
    needs pharmaverse R packages.
    """
    text = (step_description + " " + step_type).lower()

    # Check for R-required keywords
    for kw in _R_REQUIRED_KEYWORDS:
        if kw in text:
            return "r"

    # Check for Python-preferred keywords
    for kw in _PYTHON_PREFERRED_KEYWORDS:
        if kw in text:
            return "python"

    # Default: Python (more reliable for general data operations)
    return "python"


def get_snippets_for_step(
    step_description: str,
    data_catalog: List[Dict],
    language: str = "python",
) -> str:
    """Select and format relevant code snippets for a step.

    Returns a string block that can be included in the LLM prompt as
    "pre-built helper code" so the LLM doesn't have to regenerate them.
    """
    text = step_description.lower()
    snippets: List[str] = []

    # Determine data directory from catalog
    input_files = [e for e in data_catalog if e.get("source") == "input"]
    data_dir = ""
    if input_files:
        data_dir = os.path.dirname(input_files[0].get("file_path", ""))

    if language == "python":
        # Always include multi-file reader if we have a catalog
        if input_files and data_dir:
            snippets.append(PYTHON_READ_MULTI_CSV.replace("{data_dir}", data_dir))

        # Include profiling helper
        if any(kw in text for kw in ["profile", "inspect", "explore", "summary", "load"]):
            snippets.append(PYTHON_PROFILE_DF)

        # Include schema comparison if relevant
        if any(kw in text for kw in ["compare", "validate", "qc", "conformance", "ground truth"]):
            snippets.append(PYTHON_COMPARE_SCHEMAS)

    elif language == "r":
        # Include multi-file reader for R
        if input_files and data_dir:
            snippets.append(R_READ_MULTI_CSV.replace("{data_dir}", data_dir))

    if not snippets:
        return ""

    header = f"# ── Pre-built helper code ({language}) ──\n# You can use these directly. Do NOT rewrite them.\n\n"
    return header + "\n\n".join(snippets)
