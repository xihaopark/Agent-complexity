"""Error Pattern Book — curated patterns for code generation failures.

Instead of blindly retrying with raw stderr, we:
  1. Match the error against known patterns to provide *specific* fix hints
  2. Inject relevant *prevention warnings* into the LLM prompt during generation
  3. Learn new patterns within a session when a retry succeeds

Two layers:
  - Static curated patterns (this file): checked-in, grows over time
  - Session-level learned patterns (state.error_book): per-session memory
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Pattern definition ────────────────────────────────────────────────

@dataclass
class ErrorPattern:
    """A known code-generation error pattern with fix guidance."""

    id: str                           # unique identifier
    language: str                     # "r", "python", or "both"
    regex: str                        # regex to match against stderr
    title: str                        # short human-readable name
    fix_hint: str                     # specific instruction for LLM on retry
    prevention_hint: str              # warning injected during generation
    category: str = ""                # "naming", "import", "path", "type", etc.
    step_types: List[str] = field(default_factory=list)  # optional filter


# ── Curated pattern registry ──────────────────────────────────────────

PATTERNS: List[ErrorPattern] = [

    # ── R patterns ────────────────────────────────────────────────────

    ErrorPattern(
        id="r_dplyr_vector_not_function",
        language="r",
        regex=r"must be a vector, not a function",
        title="dplyr column/function name clash",
        fix_hint=(
            "A column name in your tibble clashes with a base R function name. "
            "The most common culprit is using `source` as a column name (clashes "
            "with base::source()). RENAME the column to something safe like "
            "`data_source`, `dataset_group`, or `src`. Also avoid: `data`, `c`, "
            "`t`, `T`, `F`, `list`, `matrix`, `vector`, `is`, `on`. "
            "Use .data$col_name in dplyr verbs when the name might be ambiguous."
        ),
        prevention_hint=(
            "NEVER use `source` as a column name in R (clashes with base::source()). "
            "Use `data_source` or `dataset_group` instead. "
            "Use .data$col_name in dplyr arrange/filter/mutate."
        ),
        category="naming",
    ),

    ErrorPattern(
        id="r_column_name_clash_generic",
        language="r",
        regex=r"object of type '(closure|builtin)' is not subsettable",
        title="R variable shadows a function",
        fix_hint=(
            "You assigned a variable name that shadows a base R function. "
            "Common culprits: `data`, `df`, `c`, `t`, `source`, `list`, `matrix`. "
            "Rename the variable to avoid the clash."
        ),
        prevention_hint=(
            "Avoid using `data`, `df`, `c`, `t`, `source`, `list` as variable or "
            "column names in R — they shadow base functions."
        ),
        category="naming",
    ),

    ErrorPattern(
        id="r_unexpected_end_of_input",
        language="r",
        regex=r"unexpected end of input",
        title="R code truncated / unclosed block",
        fix_hint=(
            "The R code was truncated (likely hit the token limit) or has an "
            "unclosed brace/parenthesis. Make the code MORE CONCISE: remove "
            "verbose comments, use loops instead of repetitive blocks, collapse "
            "similar operations. Target under 120 lines. Ensure all { } and ( ) "
            "are properly closed."
        ),
        prevention_hint=(
            "Keep R code under 120 lines. Use loops for repetitive operations. "
            "Ensure all braces and parentheses are closed."
        ),
        category="truncation",
    ),

    ErrorPattern(
        id="r_package_not_found",
        language="r",
        regex=r"there is no package called '(\w+)'",
        title="R package not installed",
        fix_hint=(
            "The R package is not installed. Use only packages that are commonly "
            "pre-installed: dplyr, tidyr, readr, stringr, lubridate, purrr, "
            "ggplot2, haven, admiral, tibble, forcats. If the package is not "
            "available, rewrite the code using base R or an available alternative."
        ),
        prevention_hint=(
            "Only use R packages known to be installed: tidyverse, haven, admiral, "
            "readr, lubridate. Do NOT rely on obscure packages."
        ),
        category="import",
    ),

    ErrorPattern(
        id="r_object_not_found",
        language="r",
        regex=r"object '(\w+)' not found",
        title="R object/variable not found",
        fix_hint=(
            "A variable or object was referenced before it was defined. Check: "
            "(1) Is the variable created in an earlier line? (2) Is it inside a "
            "function/tryCatch scope that doesn't export it? (3) Is the column "
            "name spelled correctly (R is case-sensitive)? (4) Did a previous "
            "step fail silently, leaving the variable undefined?"
        ),
        prevention_hint="",
        category="reference",
    ),

    ErrorPattern(
        id="r_could_not_find_function",
        language="r",
        regex=r"could not find function \"(\w+)\"",
        title="R function not found (missing library?)",
        fix_hint=(
            "A function was called without loading its package. Add the "
            "appropriate library() call at the top. Common: dplyr for mutate/"
            "filter/select, tidyr for pivot_wider/pivot_longer, stringr for "
            "str_detect, lubridate for ymd/parse_date_time, haven for read_xpt, "
            "admiral for derive_vars_*."
        ),
        prevention_hint="",
        category="import",
    ),

    ErrorPattern(
        id="r_dplyr_mutate_error",
        language="r",
        regex=r"eval_all_mutate|Problem while computing.*mutate",
        title="dplyr mutate() evaluation error",
        fix_hint=(
            "A mutate() expression failed. Common causes: (1) column name clash "
            "with a base R function — rename the column. (2) Type mismatch — check "
            "that all columns involved are the correct type (use as.numeric(), "
            "as.character(), as.Date()). (3) NA handling — use coalesce(), "
            "replace_na(), or if_else() with na-safe logic. (4) Wrong column "
            "referenced — check exact column names with names(df)."
        ),
        prevention_hint=(
            "In dplyr mutate(), always use .data$col to reference columns. "
            "Check column types before arithmetic/comparisons."
        ),
        category="dplyr",
    ),

    ErrorPattern(
        id="r_non_numeric_to_binary",
        language="r",
        regex=r"non-numeric argument to binary operator",
        title="R type mismatch in arithmetic",
        fix_hint=(
            "You tried arithmetic on a non-numeric column. Check column types "
            "with class() or str(). Convert character columns to numeric with "
            "as.numeric() before arithmetic. Date columns need special handling "
            "(as.Date / as.numeric for differences)."
        ),
        prevention_hint="",
        category="type",
    ),

    # ── Python patterns ───────────────────────────────────────────────

    ErrorPattern(
        id="py_name_error",
        language="python",
        regex=r"NameError: name ['\"](\w+)['\"] is not defined",
        title="Python NameError (forgot import or typo)",
        fix_hint=(
            "A name was used before it was defined. Most common cause: you "
            "used `os.listdir()`, `os.path.join()`, etc. without `import os` "
            "at the top of the script. ALWAYS include ALL necessary imports "
            "at the very top: `import os`, `import pandas as pd`, `import numpy "
            "as np`, etc. Check that every function and variable is either "
            "imported or defined before use."
        ),
        prevention_hint=(
            "ALWAYS start Python scripts with ALL needed imports: "
            "`import os`, `import pandas as pd`, `import numpy as np`. "
            "Never assume a module is already imported."
        ),
        category="import",
    ),

    ErrorPattern(
        id="py_name_error_import",
        language="python",
        regex=r"NameError: name '(\w+)' is not defined",
        title="Python NameError (missing import)",
        fix_hint=(
            "A name/variable was used before being defined. The most common cause "
            "is a MISSING IMPORT statement. Check: (1) Did you forget 'import os'? "
            "(2) Did you forget 'import pandas as pd'? (3) Did you forget "
            "'import numpy as np'? ALWAYS include ALL necessary import statements "
            "at the very top of the script. Required imports for typical data work: "
            "import os, import pandas as pd, import numpy as np."
        ),
        prevention_hint=(
            "ALWAYS start Python code with ALL required imports: "
            "import os, import pandas as pd, import numpy as np. "
            "Never assume any module is already imported."
        ),
        category="import",
    ),

    ErrorPattern(
        id="py_module_not_found",
        language="python",
        regex=r"ModuleNotFoundError: No module named '(\w+)'",
        title="Python module not installed",
        fix_hint=(
            "The Python module is not installed. Only use modules from the "
            "standard library or: pandas, numpy, matplotlib, seaborn, scipy, "
            "scikit-learn, openpyxl. Rewrite using available packages."
        ),
        prevention_hint=(
            "Only use standard Python packages: pandas, numpy, matplotlib, "
            "seaborn, scipy, scikit-learn. Do NOT import unavailable modules."
        ),
        category="import",
    ),

    ErrorPattern(
        id="py_file_not_found",
        language="python",
        regex=r"FileNotFoundError.*No such file or directory.*'([^']+)'",
        title="Python file path not found",
        fix_hint=(
            "The file path does not exist. Check: (1) Is the path absolute? "
            "Relative paths resolve from the artifacts/ directory. (2) Is the "
            "filename spelled correctly (case-sensitive on Linux)? (3) Use "
            "os.path.join() to build paths from PROJECT_ROOT. (4) Check the "
            "dataset_context for the correct directory and filenames."
        ),
        prevention_hint=(
            "Always `import os` at the top, then use absolute paths from "
            "the dataset context. Use os.path.join() to build paths safely."
        ),
        category="path",
    ),

    ErrorPattern(
        id="py_key_error",
        language="python",
        regex=r"KeyError: ['\"](\w+)['\"]",
        title="Python KeyError (wrong column name)",
        fix_hint=(
            "The column name does not exist in the DataFrame. Check the exact "
            "column names from the data profile (they are CASE-SENSITIVE). "
            "Use df.columns.tolist() to inspect. Common issues: extra spaces, "
            "wrong case (e.g., 'Usubjid' vs 'USUBJID'), column renamed in a "
            "previous step."
        ),
        prevention_hint=(
            "Use only column names from the data profile; they are case-sensitive. "
            "Check existence with 'col' in df.columns before use."
        ),
        category="reference",
    ),

    ErrorPattern(
        id="py_attribute_error_pandas",
        language="python",
        regex=r"AttributeError:.*('DataFrame'|'Series') object has no attribute",
        title="Pandas DataFrame/Series wrong method or attribute",
        fix_hint=(
            "You used an attribute or method that does not exist on DataFrame/Series. "
            "Check the pandas API: use .loc, .iloc, or the correct method; avoid "
            "treating a Series like a scalar. For column access use df['col'] or "
            "df.col only when the column name is a valid identifier. Check the data "
            "profile for column names and types."
        ),
        prevention_hint=(
            "When using pandas, use correct DataFrame/Series methods; check the "
            "data profile for column names and types. Use .loc/.iloc for indexing."
        ),
        category="reference",
    ),

    ErrorPattern(
        id="py_merge_key_dtype_mismatch",
        language="python",
        regex=r"merging on int and float columns where the float values are not equal to their int representation",
        title="Pandas merge key dtype mismatch (int vs float)",
        fix_hint=(
            "Before merge/compare, normalize join keys on both dataframes to the "
            "same dtype. For USUBJID/categorical keys use stripped string. For "
            "VISITNUM/AVISITN/PARAMN and *SEQ keys, convert with "
            "pd.to_numeric(errors='coerce'), round where appropriate, then cast "
            "to pandas nullable Int64. Do NOT merge raw int-vs-float keys."
        ),
        prevention_hint=(
            "Standardize QC join keys before merge: string keys as stripped str; "
            "numeric visit/seq keys as nullable Int64 on both sides."
        ),
        category="type",
    ),

    ErrorPattern(
        id="py_optional_excel_dependency_missing",
        language="python",
        regex=r"(Missing optional dependency|import_optional_dependency).*(openpyxl|xlsxwriter|xlrd)",
        title="Optional Excel dependency missing",
        fix_hint=(
            "The runtime is missing optional Excel writer/reader dependency. "
            "Avoid Excel output in this workflow step: write CSV/JSON/Markdown "
            "artifacts only and remove to_excel/read_excel code paths unless "
            "dependency is explicitly guaranteed."
        ),
        prevention_hint=(
            "Use CSV-first outputs in workflow QC/report steps; do not require "
            "openpyxl/xlsxwriter/xlrd."
        ),
        category="dependency",
    ),

    ErrorPattern(
        id="py_syntax_error",
        language="python",
        regex=r"SyntaxError: (unexpected EOF while parsing|invalid syntax)",
        title="Python syntax error / truncated code",
        fix_hint=(
            "The Python code has a syntax error, likely truncated. Make the code "
            "MORE CONCISE (under 120 lines). Ensure all parentheses, brackets, "
            "and quotes are properly closed. Remove verbose comments."
        ),
        prevention_hint=(
            "Keep Python code under 120 lines. Ensure all brackets and quotes "
            "are closed."
        ),
        category="truncation",
    ),

    ErrorPattern(
        id="py_duplicated_typeerror",
        language="python",
        regex=r"TypeError:.*DataFrame\.duplicated\(\)|duplicated\(\) got an unexpected keyword argument ['\"]dropna['\"]",
        title="DataFrame.duplicated() API mismatch (e.g. dropna not supported)",
        fix_hint=(
            "DataFrame.duplicated() in pandas 2.x does not support a dropna parameter. "
            "Use df.duplicated(subset=key_cols, keep='first') only. To ignore NaN in key columns, "
            "either fill them first (e.g. df.fillna('') for string keys) or use "
            "df.dropna(subset=key_cols).duplicated(subset=key_cols, keep='first'). "
            "Do not pass dropna= to duplicated()."
        ),
        prevention_hint=(
            "For duplicate-key checks in pandas use df.duplicated(subset=cols, keep='first') only; "
            "do not use dropna= (not supported in pandas 2.0+)."
        ),
        category="reference",
    ),

    ErrorPattern(
        id="py_tempfile_name_error",
        language="python",
        regex=r"NameError: name 'tempfile' is not defined",
        title="Python tempfile not imported",
        fix_hint=(
            "The script uses tempfile.mkdtemp() or tempfile.NamedTemporaryFile() "
            "without `import tempfile` at the top. Add `import tempfile` alongside "
            "the other stdlib imports (os, shutil, pathlib)."
        ),
        prevention_hint=(
            "When using temporary directories/files, always `import tempfile` "
            "(and `import os`, `import shutil`) at the top of the script."
        ),
        category="import",
    ),

    ErrorPattern(
        id="py_merge_key_error",
        language="python",
        regex=r"KeyError:.*(?:merge|join|concat)|MergeError",
        title="Pandas merge/join key column missing",
        fix_hint=(
            "A merge or join failed because a key column is missing on one side. "
            "Before merging, verify that all key columns exist in BOTH DataFrames: "
            "use `set(df.columns) & set(other.columns)` to find common keys. Use "
            "`how='outer'` or `how='left'` to avoid losing rows. If a key column "
            "might not exist, guard with `if col in df.columns`."
        ),
        prevention_hint=(
            "Before pd.merge(), verify join keys exist on both sides with "
            "`set(left.columns) & set(right.columns)`. Use how='outer' when "
            "columns may differ."
        ),
        category="reference",
    ),

    # ── Cross-language patterns ───────────────────────────────────────

    ErrorPattern(
        id="both_empty_csv_output",
        language="both",
        regex=r"(?:0 rows|Empty DataFrame|No data|0 observations)",
        title="Output has zero rows",
        fix_hint=(
            "The output CSV/dataset has 0 rows. This usually means: (1) A merge/"
            "join had no matching keys — check that join columns exist and have "
            "matching values in both tables (case, whitespace). (2) A filter "
            "removed all rows — print intermediate counts to debug. (3) The input "
            "data itself was empty — verify with nrow()/shape before transforms."
        ),
        prevention_hint="",
        category="logic",
    ),
]


# ── Matching API ──────────────────────────────────────────────────────

@dataclass
class MatchResult:
    """Result of matching an error against the pattern book."""

    pattern: ErrorPattern
    match: re.Match


def match_error_patterns(
    stderr: str,
    language: str = "both",
) -> List[MatchResult]:
    """Match stderr text against known error patterns.

    Returns all matching patterns, ordered by specificity (longest regex first).
    ``language`` should be "r", "python", or "both"; patterns matching the
    language OR "both" are considered.
    """
    if not stderr:
        return []

    results: List[MatchResult] = []
    for pat in PATTERNS:
        if pat.language not in (language, "both") and language != "both":
            continue
        m = re.search(pat.regex, stderr, re.IGNORECASE | re.DOTALL)
        if m:
            results.append(MatchResult(pattern=pat, match=m))

    # Sort by regex length descending (more specific patterns first)
    results.sort(key=lambda r: len(r.pattern.regex), reverse=True)
    return results


def build_fix_hint(
    stderr: str,
    language: str,
    error_book: List[Dict] = None,
) -> str:
    """Build a targeted fix hint for a retry attempt.

    Combines:
      1. Matched static patterns → specific fix_hint text
      2. Session-level learned patterns from error_book
      3. Falls back to raw stderr if nothing matches

    Returns a string to inject into the coder's retry prompt.
    """
    parts: List[str] = []

    # 1. Static pattern matches
    matches = match_error_patterns(stderr, language)
    if matches:
        parts.append("MATCHED ERROR PATTERNS (apply these fixes):")
        seen_ids = set()
        for mr in matches:
            if mr.pattern.id in seen_ids:
                continue
            seen_ids.add(mr.pattern.id)
            parts.append(f"  [{mr.pattern.title}]: {mr.pattern.fix_hint}")

    # 2. Session-level learned patterns
    if error_book:
        relevant = [
            e for e in error_book
            if e.get("language", "both") in (language, "both")
        ]
        if relevant:
            parts.append("\nPREVIOUSLY LEARNED FIXES IN THIS SESSION:")
            for entry in relevant[-5:]:  # last 5 to avoid prompt bloat
                parts.append(
                    f"  - {entry.get('title', 'Unknown')}: "
                    f"{entry.get('fix_description', '')}"
                )

    # 3. Always include raw stderr for context
    parts.append(f"\nFull error output:\n{stderr[:800]}")

    return "\n".join(parts)


# ── Prevention hints for proactive injection ──────────────────────────

def get_prevention_hints(
    language: str,
    step_type: str = "",
    error_book: List[Dict] = None,
) -> str:
    """Collect prevention hints to inject into the LLM system prompt.

    Gathers hints from:
      1. Static patterns relevant to the language/step
      2. Session-level error_book entries

    Returns a compact string (max ~20 lines) for the KNOWN PITFALLS section.
    """
    hints: List[str] = []

    # Static pattern hints
    for pat in PATTERNS:
        if pat.language not in (language, "both"):
            continue
        if not pat.prevention_hint:
            continue
        # Filter by step_type if the pattern specifies step_types
        if pat.step_types and step_type and step_type not in pat.step_types:
            continue
        hints.append(f"- {pat.prevention_hint}")

    # Session-level learned hints
    if error_book:
        relevant = [
            e for e in error_book
            if e.get("language", "both") in (language, "both")
            and e.get("prevention_hint")
        ]
        for entry in relevant[-3:]:  # limit to avoid bloat
            hints.append(f"- (Learned) {entry['prevention_hint']}")

    if not hints:
        return ""

    # De-duplicate
    seen = set()
    unique_hints = []
    for h in hints:
        if h not in seen:
            seen.add(h)
            unique_hints.append(h)

    return (
        "KNOWN PITFALLS (avoid these in your code):\n"
        + "\n".join(unique_hints[:15])  # cap at 15 lines
    )


def _tokenize_text(text: str) -> set[str]:
    if not text:
        return set()
    return {
        t for t in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]+", text.lower())
        if len(t) >= 3
    }


def query_error_book(
    error_book: List[Dict] | None,
    query_text: str,
    language: str = "both",
    limit: int = 5,
) -> List[Dict]:
    """Query session error_book for entries relevant to the current step.

    Ranking combines token overlap with recency so we can proactively inject
    only the most useful lessons into planner/coder prompts.
    """
    if not error_book:
        return []

    q_tokens = _tokenize_text(query_text)
    scored: List[tuple[float, int, Dict]] = []
    for idx, entry in enumerate(error_book):
        if not isinstance(entry, dict):
            continue
        entry_lang = str(entry.get("language", "both") or "both").lower()
        if language != "both" and entry_lang not in {language, "both"}:
            continue
        blob = " ".join([
            str(entry.get("title", "")),
            str(entry.get("fix_description", "")),
            str(entry.get("prevention_hint", "")),
            str(entry.get("stderr_snippet", "")),
            str(entry.get("category", "")),
        ])
        e_tokens = _tokenize_text(blob)
        overlap = len(q_tokens & e_tokens) if q_tokens else 0
        has_hint = 1 if entry.get("prevention_hint") else 0
        recency = idx / max(len(error_book), 1)
        score = (overlap * 10) + (has_hint * 2) + recency
        if overlap > 0 or has_hint:
            scored.append((score, idx, entry))

    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)

    picked: List[Dict] = []
    seen = set()
    for _score, _idx, entry in scored:
        key = (
            str(entry.get("title", "")),
            str(entry.get("stderr_snippet", ""))[:120],
        )
        if key in seen:
            continue
        seen.add(key)
        picked.append(entry)
        if len(picked) >= max(1, limit):
            break
    return picked


def format_error_book_lessons(entries: List[Dict] | None, max_items: int = 3) -> str:
    """Format queried error-book entries into concise LLM-friendly lessons."""
    if not entries:
        return ""
    lines: List[str] = []
    for entry in entries[:max_items]:
        title = str(entry.get("title", "Known issue")).strip()
        fix = str(entry.get("fix_description", "")).strip()
        hint = str(entry.get("prevention_hint", "")).strip()
        category = str(entry.get("category", "")).strip()
        parts = [f"- {title}"]
        if category:
            parts.append(f"[{category}]")
        if fix:
            parts.append(f"Fix: {fix[:220]}")
        if hint:
            parts.append(f"Prevent: {hint[:180]}")
        lines.append(" ".join(parts))

    if not lines:
        return ""
    return "LESSONS FROM ERROR BOOK (apply proactively):\n" + "\n".join(lines)
