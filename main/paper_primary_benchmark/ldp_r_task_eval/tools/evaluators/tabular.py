"""Tabular comparison helpers.

Loads TSV/CSV/whitespace-separated files with a series of fallbacks, then
produces either:

* a canonical CSV form (for the ``normalized_text_equal`` tier) or
* a match fraction (for the ``tabular_tolerance`` tier).
"""

from __future__ import annotations

import csv
import io
import math
from pathlib import Path

import numpy as np
import pandas as pd


_TRY_SEPS = ["\t", ",", ";", "|"]


def _sniff_sep(text: str) -> str | None:
    """Sniff a CSV-ish separator from the first non-empty line."""
    first = next((ln for ln in text.splitlines() if ln.strip()), "")
    if not first:
        return None
    try:
        dialect = csv.Sniffer().sniff(first, delimiters="".join(_TRY_SEPS))
        if dialect.delimiter in _TRY_SEPS:
            return dialect.delimiter
    except Exception:
        pass
    for sep in _TRY_SEPS:
        if sep in first:
            return sep
    return None


def load_table(path: Path) -> pd.DataFrame | None:
    """Try hard to load ``path`` as a DataFrame.

    Returns ``None`` when the file clearly isn't a tabular text blob.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    if not text.strip():
        return None

    sep = _sniff_sep(text)
    attempts: list[tuple[str | None, bool]] = []
    if sep:
        attempts.append((sep, True))
        attempts.append((sep, False))
    attempts.extend([
        ("\t", True), ("\t", False),
        (",", True), (",", False),
        (r"\s+", True), (r"\s+", False),
    ])
    seen: set[tuple[str | None, bool]] = set()
    for sep_try, has_header in attempts:
        key = (sep_try, has_header)
        if key in seen:
            continue
        seen.add(key)
        try:
            df = pd.read_csv(
                io.StringIO(text),
                sep=sep_try,
                header=0 if has_header else None,
                engine="python",
                dtype=str,
                keep_default_na=False,
                na_values=["", "NA", "NaN", "nan", "None"],
                on_bad_lines="skip",
            )
        except Exception:
            continue
        if df.shape[1] >= 1 and df.shape[0] >= 1:
            df.columns = [str(c).strip() for c in df.columns]
            return df
    return None


def _to_numeric(val: object) -> float | None:
    if val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        s = str(val).strip().strip('"').strip("'")
        if not s or s.upper() in {"NA", "NAN", "NONE"}:
            return None
        try:
            return float(s)
        except ValueError:
            return None


def _clean_str(val: object) -> str:
    if val is None:
        return ""
    if isinstance(val, float) and math.isnan(val):
        return ""
    return str(val).strip().strip('"').strip("'")


def _first_non_numeric_col(df: pd.DataFrame) -> str | None:
    """Pick the leftmost non-numeric column with reasonable cardinality.

    A column that is constant (e.g. methylKit's ``__item__`` prefix) is
    useless for row alignment, so we keep looking for one with enough
    distinct values to actually order rows.
    """
    n = len(df)
    if n == 0:
        return None
    for col in df.columns:
        series = df[col].head(min(64, n))
        non_numeric = [v for v in series if _to_numeric(v) is None and _clean_str(v) != ""]
        if not non_numeric:
            continue
        distinct = len(set(_clean_str(v) for v in df[col]))
        if distinct < max(2, min(4, n // 16)):
            continue
        return col
    return None


def canonical_tsv(df: pd.DataFrame, float_format: str = "%.6g") -> str:
    """Deterministic CSV form of a DataFrame for equality checks."""
    out = df.copy()
    key_col = _first_non_numeric_col(out)
    if key_col is not None:
        out = out.sort_values(by=[key_col, *[c for c in out.columns if c != key_col]], kind="mergesort")
    else:
        out = out.sort_values(by=list(out.columns), kind="mergesort")
    out = out.reset_index(drop=True)
    buf = io.StringIO()
    out.to_csv(buf, index=False, sep="\t", float_format=float_format, lineterminator="\n")
    return buf.getvalue()


def _bucket(val: object, rtol: float, atol: float) -> str:
    """Render a cell so numerically-close values hash to the same string."""
    n = _to_numeric(val)
    if n is not None:
        if math.isnan(n):
            return "NA"
        if n == 0.0:
            return "0"
        scale = max(abs(n) * rtol, atol)
        if scale <= 0:
            return f"{n:.6g}"
        bucket = round(n / scale)
        return f"b:{bucket}"
    return "s:" + _clean_str(val)


def tabular_tolerance_score(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    rtol: float = 1e-3,
    atol: float = 1e-5,
) -> dict:
    """Compare two DataFrames.

    Strategy:
      1. Align columns by name (shared subset) or by position when that
         produces similar cardinality.
      2. Fingerprint each row using :func:`_bucket` so numerically-close
         cells collapse to the same token.
      3. Count how many rows of A appear in B (as a multiset intersection).
      4. Compute cell-level match fraction across aligned rows as a
         secondary signal.
      5. Combine into an ``effective_fraction`` with mild penalties for
         column-count and row-count mismatches.
    """
    cols_a = list(df_a.columns)
    cols_b = list(df_b.columns)
    shared = [c for c in cols_a if c in cols_b]

    if shared and len(shared) >= max(1, min(len(cols_a), len(cols_b)) // 2):
        ref_cols = shared
        aligned_a = df_a[ref_cols].copy()
        aligned_b = df_b[ref_cols].copy()
        alignment = "by_name"
    else:
        ncols = min(len(cols_a), len(cols_b))
        aligned_a = df_a.iloc[:, :ncols].copy()
        aligned_b = df_b.iloc[:, :ncols].copy()
        aligned_a.columns = list(range(ncols))
        aligned_b.columns = list(range(ncols))
        ref_cols = list(range(ncols))
        alignment = "by_position"

    def _fingerprints(df: pd.DataFrame) -> list[tuple[str, ...]]:
        rows: list[tuple[str, ...]] = []
        for _, row in df.iterrows():
            rows.append(tuple(_bucket(row[c], rtol, atol) for c in ref_cols))
        return rows

    fp_a = _fingerprints(aligned_a)
    fp_b = _fingerprints(aligned_b)

    from collections import Counter

    counter_b = Counter(fp_b)
    rows_matched = 0
    for fp in fp_a:
        if counter_b.get(fp, 0) > 0:
            rows_matched += 1
            counter_b[fp] -= 1

    denom_rows = max(len(fp_a), len(fp_b)) or 1
    row_match_fraction = rows_matched / denom_rows

    sorted_a = sorted(fp_a)
    sorted_b = sorted(fp_b)
    nrows = min(len(sorted_a), len(sorted_b))
    cells_total = 0
    cells_matched = 0
    for ra, rb in zip(sorted_a[:nrows], sorted_b[:nrows]):
        for a_cell, b_cell in zip(ra, rb):
            cells_total += 1
            if a_cell == b_cell:
                cells_matched += 1
    cell_match_fraction = (cells_matched / cells_total) if cells_total else 0.0

    row_overlap = (
        nrows / max(len(sorted_a), len(sorted_b)) if max(len(sorted_a), len(sorted_b)) else 0.0
    )

    col_overlap = (
        len(ref_cols) / max(len(cols_a), len(cols_b)) if max(len(cols_a), len(cols_b)) else 0.0
    )
    cols_mismatch = len(cols_a) != len(cols_b)
    # V2.1: relax column penalty. If the reference schema is fully covered by the
    # agent (superset) or shared cols span >=80% of the smaller side, only apply
    # a mild 0.9 penalty. Hard 0.7*col_overlap was tanking 80% cell-match cases
    # where the agent merely added an extra annotation column.
    min_cols = min(len(cols_a), len(cols_b)) or 1
    covers_smaller = len(ref_cols) >= min_cols  # shared columns span the smaller schema
    if not cols_mismatch:
        col_penalty = 1.0
    elif covers_smaller:
        col_penalty = 0.95
    elif col_overlap >= 0.8:
        col_penalty = 0.9
    else:
        col_penalty = max(0.7 * col_overlap, 0.5)

    effective = max(row_match_fraction, cell_match_fraction * row_overlap) * col_penalty

    return {
        "alignment": alignment,
        "cols_a": len(cols_a),
        "cols_b": len(cols_b),
        "cols_shared": len(ref_cols),
        "rows_a": len(df_a),
        "rows_b": len(df_b),
        "rows_matched": rows_matched,
        "row_match_fraction": row_match_fraction,
        "cells_matched": cells_matched,
        "cells_total": cells_total,
        "cell_match_fraction": cell_match_fraction,
        "row_overlap": row_overlap,
        "effective_fraction": effective,
        "cols_mismatch": cols_mismatch,
    }
