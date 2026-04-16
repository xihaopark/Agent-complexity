"""coder node — LLM-powered code generation for analysis steps.

Takes the current step description and data profile, calls the LLM to
generate executable code (Python or R) and places it in code_scratchpad
for the executor to run.

Language selection:
  - CDISC/SDTM/ADaM/TLF clinical tasks -> R (pharmaverse ecosystem)
  - General data analysis -> Python (pandas/numpy ecosystem)

On retry (after validation failure), the previous error is included in the
prompt so the LLM can fix the issue.
"""
from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage

from renzo.app.state import AgentState
from renzo.app.llm import get_llm
from renzo.app.nodes.data_analyst import build_catalog_summary
from renzo.app.code_snippets import select_language_for_step, get_snippets_for_step
from renzo.app.error_patterns import (
    format_error_book_lessons,
    get_prevention_hints,
    query_error_book,
)
from renzo.app.tracing import append_trace, build_llm_trace_entry

logger = logging.getLogger(__name__)

# ── Prompt templates ──────────────────────────────────────────────────

_CODE_SYSTEM_PROMPT = """\
You are a data analysis code generator that writes executable Python or R code.
IMPORTANT: All comments, print statements, and output text must be in English.
Choose the language based on the task:

LANGUAGE SELECTION:
  - Use R for clinical trial / pharmaceutical tasks:
    CDISC standards (SDTM, ADaM), TLF generation, XPT file handling,
    regulatory submissions, pharmaverse workflows.
  - Use Python for general data analysis:
    CSV/Excel processing, machine learning, general statistics, visualizations.
  - If the step explicitly requests a language, use that language.

PYTHON RULES:
  - ALWAYS start with ALL necessary imports: import os, import pandas as pd, etc.
    Never assume any module is pre-imported. Every script must be self-contained.
  - Use pandas, numpy, matplotlib, seaborn, scipy as needed.
  - Save ALL outputs (CSV, PNG, etc.) to the working directory (current dir).
  - Default to CSV/JSON/Markdown outputs. Do NOT write .xlsx/.xls files unless
    explicitly required by the step, and avoid optional Excel dependencies.
  - Use descriptive filenames like "summary_stats.csv", "distribution_plot.png".
  - Print key results to stdout so the user can see them.
  - Do NOT use subprocess, os.system, or make network requests.
  - Do NOT use interactive features (plt.show() — use plt.savefig() instead).
  - Handle errors gracefully with try/except where appropriate.
  - Output code inside a ```python code fence.

DATA AND PANDAS (Python):
  - Before using a column, ensure it exists: e.g. df.columns.tolist() or 'col' in df.columns.
    Column names from the data profile are case-sensitive and may contain spaces.
  - For merges/joins, use exact column names from the provided data context; normalize dtypes
    (e.g. string strip, numeric) when joining.
  - Handle missing/NaN: use .fillna() or .dropna() as appropriate; do not assume no nulls.
  - Prefer explicit column lists when selecting (e.g. df[['A','B']]) and avoid chaining
    on possibly missing columns.
  - For duplicate-key checks use df.duplicated(subset=cols, keep='first') only; do not
    pass dropna= to duplicated() (not supported in pandas 2.x).
  - When using temporary directories import tempfile (and os, shutil) at the top of the
    script. Never assume stdlib modules are pre-imported.
  - Before pd.merge()/join, verify key columns exist on BOTH sides:
    common = list(set(left.columns) & set(right.columns) & set(key_cols)).
    Use how='outer' or how='left' when schemas may differ. Guard with
    `if col in df.columns` for optional columns.

R RULES:
  - Start R code with the marker line: #!R
  - Use pharmaverse packages: admiral (ADaM derivation), haven (XPT I/O),
    metacore/metatools (metadata), xportr (XPT export with attributes).
  - Use tidyverse for data wrangling: dplyr, tidyr, stringr, lubridate.
  - For TLF generation: rtables, gtsummary, gt, ggplot2, Tplyr.
  - Save outputs to working directory: write_xpt(), write.csv(), ggsave().
  - Prefer CSV/Markdown outputs; avoid Excel writer dependencies in workflow QC/report steps.
  - Print key results with cat() or print().
  - Handle errors with tryCatch() where appropriate.
  - Output code inside a ```r code fence with #!R as the first line.

GENERAL:
  - The input data file path will be provided — use it directly.
  - IMPORTANT: If a relative path like "workflow_pool/..." or "data/..." is
    mentioned, convert it to an absolute path using the PROJECT_ROOT provided.
    The code runs from the artifacts/ directory, NOT the project root.
  - Save all outputs to the current working directory (artifacts/).
  - Output ONLY the code inside a single code fence, no explanation.
  - KEEP CODE CONCISE. Avoid boilerplate. Do NOT write separate helper functions
    for things like safe-reading each file. Use loops where possible.
    Target under 150 lines of code. If a step involves many files, iterate
    over a list rather than writing separate code for each file.

Example Python output:
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/path/to/data.csv")
print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
df_result.to_csv("analysis_result.csv", index=False)
plt.savefig("analysis_plot.png", dpi=150, bbox_inches="tight")
print("Done. Outputs: analysis_result.csv, analysis_plot.png")
```

Example R output:
```r
#!R
library(haven)
library(dplyr)
library(admiral)

dm <- read_xpt("/path/to/dm.xpt")
cat("DM dataset:", nrow(dm), "rows,", ncol(dm), "columns\\n")
adsl <- dm %>%
  select(STUDYID, USUBJID, SUBJID, SITEID, AGE, AGEU, SEX, RACE, ARM, ACTARM) %>%
  derive_vars_merged(dataset_add = ex, by_vars = exprs(STUDYID, USUBJID))
write_xpt(adsl, "adsl.xpt")
cat("Done. Output: adsl.xpt\\n")
```
"""

_R_DOMAIN_CONTEXT = """\

CLINICAL TRIAL DOMAIN KNOWLEDGE:
You are working with CDISC-standard clinical trial data. Key concepts:
  - SDTM (Study Data Tabulation Model): Raw study data organized by domains
    (DM=Demographics, AE=Adverse Events, EX=Exposure, VS=Vital Signs, LB=Lab, etc.)
  - ADaM (Analysis Data Model): Analysis-ready datasets derived from SDTM
    (ADSL=Subject-Level, ADAE=AE Analysis, ADLB=Lab Analysis, ADTTE=Time-to-Event, etc.)
  - TLF: Tables, Listings, and Figures for clinical study reports
  - XPT: SAS Transport format, the standard file format for regulatory submissions
  - Dataset-JSON: New JSON-based alternative to XPT for CDISC data exchange

Key R packages for this pipeline:
  - admiral: Primary package for ADaM dataset derivation from SDTM
  - haven: Read/write SAS XPT files (read_xpt, write_xpt)
  - metacore/metatools: Metadata-driven CDISC workflows
  - xportr: Apply dataset attributes and export compliant XPT files
  - rtables / gtsummary / gt: Generate formatted clinical tables
  - ggplot2: Publication-quality figures
  - diffdf: Compare datasets for QC/validation
"""

_RETRY_ADDENDUM = """
IMPORTANT: The previous code attempt FAILED with this error:
{stderr}

Fix the issue in your new code. Do NOT repeat the same mistake.
Common fixes: missing imports/library(), wrong column names, wrong file paths,
type errors, unclosed brackets, column-name clashes with built-in functions.
"""

def _should_use_r(step_description: str, data_profile: Dict) -> bool:
    """Determine if R should be used for this step.

    Now delegates to the smarter per-step language selector in code_snippets.
    R is only chosen when pharmaverse packages (admiral, xportr, etc.) are
    actually needed. Data reading, profiling, and general analysis default
    to Python.
    """
    step_type = ""
    # Check data file extension — XPT files need R's haven
    file_path = data_profile.get("file_path", "").lower()
    if file_path.endswith(".xpt"):
        return True
    lang = select_language_for_step(step_description, step_type)
    return lang == "r"


def _extract_code_block(text: str) -> Optional[str]:
    """Extract code from a markdown code fence (Python or R).

    Handles various fence formats: ```python, ```r, ```R, ```{r},
    ```bash, or bare ```.  Falls back to scanning for code markers
    like #!R or import statements anywhere in the text.
    """
    # 1. Try fenced code block with ANY language tag (```python, ```r, ```{r}, ```bash, etc.)
    pattern = r"```[\w{}\s]*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        if code:
            return code

    # 2. If no fence, try to use the whole response if it starts with code
    lines = text.strip().splitlines()
    if lines and (
        lines[0].startswith("import ")
        or lines[0].startswith("from ")
        or lines[0].startswith("#!R")
        or lines[0].startswith("library(")
    ):
        return text.strip()

    # 3. Last resort: scan for #!R or library( marker anywhere in text
    #    (LLM may have wrapped code in explanatory prose)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "#!R" or stripped.startswith("library(") or stripped.startswith("import pandas"):
            # Return from this line to the end
            code = "\n".join(lines[i:]).strip()
            if code:
                logger.info("Extracted code via line-scan fallback (line %d)", i)
                return code

    logger.warning("Code extraction failed. LLM response preview: %.300s", text[:300])
    return None


def _auto_fix_python_imports(code: str) -> str:
    """Auto-inject missing standard imports in generated Python code.

    The LLM frequently forgets `import os` or `import pandas as pd`
    despite explicit instructions. This function detects usage of common
    modules and injects the import if missing.
    """
    if code.strip().startswith("#!R"):
        return code  # R code, skip

    lines = code.split("\n")
    # Collect all existing import lines
    import_lines = {l.strip() for l in lines if l.strip().startswith("import ") or l.strip().startswith("from ")}

    missing_imports = []

    # Check for os usage without import
    if re.search(r"\bos\.", code) and "import os" not in import_lines:
        missing_imports.append("import os")

    # Check for sys usage without import
    if re.search(r"\bsys\.", code) and "import sys" not in import_lines:
        missing_imports.append("import sys")

    # Check for pd usage without import
    if re.search(r"\bpd\.", code) and "import pandas as pd" not in import_lines:
        missing_imports.append("import pandas as pd")

    # Check for np usage without import
    if re.search(r"\bnp\.", code) and "import numpy as np" not in import_lines:
        missing_imports.append("import numpy as np")

    # Check for plt usage without import
    if re.search(r"\bplt\.", code) and "import matplotlib.pyplot as plt" not in import_lines:
        missing_imports.append("import matplotlib.pyplot as plt")

    # Check for json usage without import
    if re.search(r"\bjson\.", code) and "import json" not in import_lines:
        missing_imports.append("import json")

    # Check for glob usage without import
    if re.search(r"\bglob\.", code) and "import glob" not in import_lines:
        missing_imports.append("import glob")

    # Check for tempfile usage without import
    if re.search(r"\btempfile\.", code) and "import tempfile" not in import_lines:
        missing_imports.append("import tempfile")

    # Check for subprocess usage without import
    if re.search(r"\bsubprocess\.", code) and "import subprocess" not in import_lines:
        missing_imports.append("import subprocess")

    # Check for shutil usage without import
    if re.search(r"\bshutil\.", code) and "import shutil" not in import_lines:
        missing_imports.append("import shutil")

    if missing_imports:
        logger.warning("Auto-injecting missing imports: %s", missing_imports)
        # Insert after any existing imports, or at the top
        insert_block = "\n".join(missing_imports)
        # Find the last import line index
        last_import_idx = -1
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                last_import_idx = i
        if last_import_idx >= 0:
            lines.insert(last_import_idx + 1, insert_block)
        else:
            lines.insert(0, insert_block)
        code = "\n".join(lines)

    return code


def _build_data_context(data_profile: Dict, data_catalog: list = None) -> str:
    """Build data context string for LLM prompts.

    Prefers the rich ``data_catalog`` if available; falls back to the
    legacy ``data_profile`` dict for backward compatibility.
    """
    # If we have a rich catalog, use it (includes all files, columns, keys, samples)
    if data_catalog:
        return "\n\n" + build_catalog_summary(data_catalog, include_samples=True)

    # Legacy fallback using data_profile
    if not data_profile:
        return ""

    file_path = data_profile.get("file_path", "")
    sample = data_profile.get("sample", {})
    sample_str = ""
    if sample:
        try:
            cols = list(sample.keys())
            rows = []
            if cols:
                n_rows = len(sample[cols[0]]) if sample[cols[0]] else 0
                for i in range(min(n_rows, 3)):
                    row = {c: sample[c][i] for c in cols}
                    rows.append(row)
            sample_str = json.dumps(rows, indent=2, default=str)
        except Exception:
            sample_str = str(sample)[:500]

    context = (
        f"\n\nData file: {file_path}\n"
        f"Shape: {data_profile.get('rows', '?')} rows x {data_profile.get('columns', '?')} columns\n"
        f"Column types:\n{json.dumps(data_profile.get('dtypes', {}), indent=2, default=str)}\n"
        f"Missing values:\n{json.dumps(data_profile.get('missing', {}), indent=2, default=str)}\n"
        f"Sample rows:\n{sample_str}\n"
    )

    # Include multi-file inventory if available (experiment datasets)
    all_files = data_profile.get("all_files", [])
    if all_files:
        context += f"\nAll available data files ({len(all_files)}):\n"
        for af in all_files:
            domain = af.get("domain", "")
            domain_str = f" ({domain})" if domain else ""
            context += f"  - {af.get('filename', '?')}{domain_str}: {af['path']}\n"

    return context


def _generate_code_via_llm(
    step_description: str,
    data_profile: Dict,
    know_how: str = "",
    prefer_r: bool = False,
    previous_error: Optional[str] = None,
    targeted_fix_hint: Optional[str] = None,
    dataset_context: str = "",
    data_catalog: list = None,
    error_book: list = None,
    step_type: str = "",
    execution_workdir: str = "",
    step_id: str = "",
) -> tuple[Optional[str], Dict[str, Any]]:
    """Call the LLM to generate Python or R analysis code."""
    prompt_messages = []
    llm = None
    try:
        llm = get_llm(temperature=0.2, max_tokens=8192)

        language = "r" if prefer_r else "python"

        # Build system prompt with optional domain context
        system_prompt = _CODE_SYSTEM_PROMPT
        if prefer_r:
            system_prompt += _R_DOMAIN_CONTEXT
        if know_how:
            system_prompt += f"\n\nADDITIONAL DOMAIN KNOWLEDGE:\n{know_how[:4000]}\n"

        # Inject prevention hints from the Error Pattern Book
        pitfalls = get_prevention_hints(language, step_type, error_book)
        if pitfalls:
            system_prompt += f"\n\n{pitfalls}\n"

        # Query learned session mistakes for this exact step and inject concise lessons.
        lesson_query = " ".join([
            step_description or "",
            previous_error or "",
            targeted_fix_hint or "",
            step_type or "",
        ])
        matched_lessons = query_error_book(
            error_book=error_book or [],
            query_text=lesson_query,
            language=language,
            limit=4,
        )
        lessons_text = format_error_book_lessons(matched_lessons, max_items=3)
        if lessons_text:
            system_prompt += f"\n\n{lessons_text}\n"

        # Build user message — prefer rich catalog over legacy profile
        data_context = _build_data_context(data_profile, data_catalog=data_catalog)
        lang_name = "R" if prefer_r else "Python"
        language_hint = f"\n\nPreferred language: {lang_name}."
        if prefer_r:
            language_hint += " You MUST generate R code (starting with #!R)."
        else:
            language_hint += " Generate Python code."

        # Include project root so LLM can construct absolute paths
        project_root = os.environ.get("RENZO_PROJECT_ROOT", os.getcwd())
        effective_working_dir = execution_workdir or os.path.join(project_root, "renzo", "data", "artifacts")
        path_context = (
            f"\n\nPROJECT_ROOT: {project_root}"
            f"\nWORKING_DIR: {effective_working_dir}"
            f"\nFor any relative file paths like 'workflow_pool/...', use "
            f"file.path('{project_root}', 'workflow_pool', ...) in R or "
            f"os.path.join('{project_root}', ...) in Python."
        )

        # Include dataset context so the coder knows exactly where data files are
        dataset_section = ""
        if dataset_context:
            dataset_section = f"\n\n{dataset_context}"

        # Inject pre-built code snippets so the LLM doesn't regenerate them
        snippets_section = ""
        if data_catalog:
            snippets = get_snippets_for_step(
                step_description, data_catalog,
                language=language,
            )
            if snippets:
                snippets_section = (
                    f"\n\nPRE-BUILT HELPER CODE (use these directly, do NOT rewrite):\n"
                    f"```\n{snippets}\n```"
                )

        user_msg = f"Step: {step_description}{data_context}{dataset_section}{language_hint}{path_context}{snippets_section}"
        if data_context and not prefer_r:
            user_msg += "\n\nUse only column names from the data context above; check that each column exists (e.g. 'col' in df.columns) before use."

        # On retry: use the targeted fix hint from the Error Pattern Book
        # instead of the generic retry addendum
        if previous_error:
            if targeted_fix_hint:
                user_msg += (
                    f"\n\nIMPORTANT: The previous code attempt FAILED.\n"
                    f"{targeted_fix_hint}"
                )
            else:
                user_msg += _RETRY_ADDENDUM.format(stderr=previous_error[:800])

        prompt_messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_msg),
        ]
        response = llm.invoke(prompt_messages)

        code = _extract_code_block(response.content)
        trace_entry = build_llm_trace_entry(
            node="coder",
            purpose="generate_code",
            prompt_messages=prompt_messages,
            response=response,
            status="success" if code else "parse_failed",
            parsed_output={
                "code_extracted": bool(code),
                "language": language,
                "step_type": step_type,
            },
            context={
                "step_id": step_id,
                "step_description": step_description[:500],
                "previous_error": (previous_error or "")[:500],
            },
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )
        if code:
            # Auto-fix missing imports before returning
            code = _auto_fix_python_imports(code)
            logger.info("LLM generated %d lines of code (R=%s)", len(code.splitlines()), prefer_r)
            return code, trace_entry
        else:
            logger.warning("Failed to extract code from LLM response")
            return None, trace_entry

    except Exception as e:
        logger.error("LLM code generation failed: %s", e)
        return None, build_llm_trace_entry(
            node="coder",
            purpose="generate_code",
            prompt_messages=prompt_messages,
            response=None,
            status="error",
            parsed_output=None,
            error=str(e),
            context={
                "step_id": step_id,
                "step_description": step_description[:500],
                "step_type": step_type,
            },
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )


def _ensure_python_imports(code: str) -> str:
    """Post-process Python code to guarantee critical imports exist.

    LLMs frequently forget 'import os' or 'import pandas as pd' even when
    prompted.  This deterministic pass scans for usage and injects missing
    imports at the top of the script — a cheap safety net that prevents the
    single most common class of NameError failures.
    """
    lines = code.split("\n")
    # Collect existing import lines (first 40 lines to avoid false positives)
    head = "\n".join(lines[:40])

    needed: list[str] = []

    # os
    if re.search(r"\bos\.", code) and not re.search(r"^\s*import\s+os\b", head, re.M):
        needed.append("import os")

    # pandas
    if re.search(r"\bpd\.", code) and not re.search(r"^\s*(import\s+pandas|from\s+pandas)", head, re.M):
        needed.append("import pandas as pd")

    # numpy
    if re.search(r"\bnp\.", code) and not re.search(r"^\s*(import\s+numpy|from\s+numpy)", head, re.M):
        needed.append("import numpy as np")

    # glob
    if re.search(r"\bglob\.", code) and not re.search(r"^\s*import\s+glob\b", head, re.M):
        needed.append("import glob")

    # json
    if re.search(r"\bjson\.", code) and not re.search(r"^\s*import\s+json\b", head, re.M):
        needed.append("import json")

    # datetime
    if re.search(r"\bdatetime\.", code) and not re.search(r"^\s*(import\s+datetime|from\s+datetime)", head, re.M):
        needed.append("import datetime")

    # re
    if re.search(r"\bre\.(search|match|sub|findall|compile)\b", code) and not re.search(r"^\s*import\s+re\b", head, re.M):
        needed.append("import re")

    if not needed:
        return code

    logger.info("Auto-injecting missing Python imports: %s", needed)
    import_block = "\n".join(needed) + "\n"

    # Insert after any existing leading comments / shebangs, before first real code
    insert_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            insert_idx = i + 1
        else:
            break

    lines.insert(insert_idx, import_block)
    return "\n".join(lines)


def _parse_first_path_from_context(dataset_context: str) -> str:
    """Extract the first file path from a dataset_context string.

    Looks for lines like:
      Directory: /abs/path/to/ds-xxx/files/
      Files (20): dm.csv, ae.csv, ...
    and combines them into a usable path.
    """
    directory = ""
    for line in dataset_context.splitlines():
        stripped = line.strip()
        if stripped.startswith("Directory:"):
            directory = stripped.split("Directory:", 1)[1].strip()
        elif stripped.startswith("Files") and directory:
            # Extract the first filename from "Files (N): dm.csv, ae.csv, ..."
            colon_idx = stripped.find(":")
            if colon_idx >= 0:
                files_part = stripped[colon_idx + 1:].strip()
                first_file = files_part.split(",")[0].strip()
                if first_file:
                    return os.path.join(directory, first_file)
    return ""


def _fallback_code(data_profile: Dict, prefer_r: bool = False, dataset_context: str = "") -> str:
    """Generate simple fallback code when LLM is unavailable."""
    file_path = data_profile.get("file_path", "")
    # Also check multi-file inventory for a usable path
    if not file_path:
        all_files = data_profile.get("all_files", [])
        if all_files:
            file_path = all_files[0].get("path", "")
    # Last resort: parse file path from dataset_context text
    if not file_path and dataset_context:
        file_path = _parse_first_path_from_context(dataset_context)
    if not file_path:
        file_path = "data.csv"
    ext = os.path.splitext(file_path)[1].lower()

    # Choose the correct reader based on file extension
    if prefer_r or ext == ".xpt":
        read_fn = "read_xpt" if ext == ".xpt" else "read.csv"
        lib_line = "library(haven)\n" if ext == ".xpt" else ""
        return f"""#!R
{lib_line}
df <- {read_fn}("{file_path}")
cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\\n")
cat("\\nColumn names:\\n")
cat(paste(names(df), collapse=", "), "\\n")
cat("\\nFirst 5 rows:\\n")
print(head(df, 5))
cat("\\nSummary:\\n")
print(summary(df))
write.csv(df, "summary_output.csv", row.names=FALSE)
cat("\\nDone. Output: summary_output.csv\\n")
"""

    return f"""import pandas as pd

df = pd.read_csv(r"{file_path}")
print(f"Dataset shape: {{df.shape}}")
print("\\nColumn types:")
print(df.dtypes)
print("\\nBasic statistics:")
print(df.describe(include='all'))
print("\\nMissing values:")
print(df.isna().sum())
df.describe(include='all').to_csv("summary_stats.csv")
print("\\nDone. Output: summary_stats.csv")
"""


# ── Main coder node ───────────────────────────────────────────────────

def coder_node(state: AgentState) -> Dict:
    """Generate executable Python or R code for the current analysis step."""
    data_profile = state.get("data_profile", {})
    plan_steps = state.get("plan_steps", [])
    current_step_id = state.get("current_step_id")
    know_how = state.get("know_how_context", "")
    goal = state.get("goal", "")
    ds_ctx = state.get("dataset_context", "")
    execution_workdir = state.get("execution_workdir", "")
    llm_trace = list(state.get("llm_trace") or [])

    # Find the current step description and preferred language from plan
    step_description = "Analyze the data and produce summary statistics"
    step_language = None
    for step in plan_steps:
        if step.get("id") == current_step_id:
            step_description = step.get("description", step_description)
            step_language = step.get("language")  # "r" or "python" from planner
            break

    # Determine preferred language — smart per-step selection is primary.
    # Only use R when the step genuinely needs pharmaverse packages
    # (admiral, xportr, etc.). Data reading, profiling, QC → Python.
    # The planner's "language" hint is advisory but select_language_for_step()
    # is the authoritative decision-maker based on actual step content.
    step_type = ""
    for step in plan_steps:
        if step.get("id") == current_step_id:
            step_type = step.get("type", "")
            break
    lang = select_language_for_step(step_description, step_type)
    prefer_r = (lang == "r")
    logger.info("Language auto-selected: %s for step '%s'", lang, step_description[:60])
    logger.info("Language decision: prefer_r=%s (planner hint was: %s)", prefer_r, step_language)

    # Build a rich step description that includes the user's goal context
    # so the LLM knows the file paths and specific requirements
    full_step_context = step_description
    if goal and goal != step_description:
        full_step_context = (
            f"Step: {step_description}\n\n"
            f"User's original request (use file paths and details from this):\n{goal}"
        )
    # When the workflow step declares expected outputs, append so the coder produces only those files
    for step in plan_steps:
        if step.get("id") == current_step_id and step.get("outputs"):
            outputs_list = step["outputs"]
            if isinstance(outputs_list, list) and outputs_list:
                full_step_context += (
                    "\n\nExpected output files for this step: "
                    + ", ".join(str(x) for x in outputs_list)
                    + ". Produce only these; use a temp subdirectory for any intermediate files."
                )
            break

    # Check if this is a retry (validation failure with error context)
    previous_error = None
    targeted_fix_hint = None
    validation = state.get("validation_result", {})
    if validation.get("status") == "failed":
        previous_error = validation.get("stderr_excerpt", "")
        # Use the targeted fix hint from Error Pattern Book if available
        targeted_fix_hint = validation.get("targeted_fix_hint", "")
        matched_ids = validation.get("matched_pattern_ids", [])
        if matched_ids:
            logger.info("Retry with Error Pattern Book hints: %s", matched_ids)

    # Resolve step_type for pattern prevention hints
    step_type = ""
    for step in plan_steps:
        if step.get("id") == current_step_id:
            step_type = step.get("type", "")
            break

    # Generate code via LLM
    catalog = state.get("data_catalog", [])
    error_book = state.get("error_book", [])
    code, llm_entry = _generate_code_via_llm(
        full_step_context, data_profile,
        know_how=know_how,
        prefer_r=prefer_r,
        previous_error=previous_error,
        targeted_fix_hint=targeted_fix_hint,
        dataset_context=ds_ctx,
        data_catalog=catalog or None,
        error_book=error_book or None,
        step_type=step_type,
        execution_workdir=execution_workdir,
        step_id=current_step_id or "",
    )
    llm_trace = append_trace(llm_trace, llm_entry)

    # Fallback to basic code if LLM fails
    if not code:
        logger.warning("Using fallback code generation")
        code = _fallback_code(data_profile, prefer_r=prefer_r, dataset_context=ds_ctx)

    # Detect language for state
    language = "r" if (code.strip().startswith("#!R") or code.strip().startswith("# R code")) else "python"

    # Post-process: deterministically ensure critical Python imports are present
    if language == "python":
        code = _ensure_python_imports(code)

    return {
        "code_scratchpad": code,
        "code_language": language,
        "llm_trace": llm_trace,
        "next_node": "executor",
    }
