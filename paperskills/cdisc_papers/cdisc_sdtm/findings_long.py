from __future__ import annotations

from typing import Iterable, Mapping, Sequence

import pandas as pd


def pivot_to_sdtm_findings_long(
    df: pd.DataFrame,
    *,
    id_cols: Sequence[str],
    item_cols: Iterable[str] | None = None,
    item_to_test: Mapping[str, str] | None = None,
    item_colname: str = "ITEM",
    result_colname: str = "RESULT",
    drop_missing: bool = True,
) -> pd.DataFrame:
    """Convert wide CRF-style columns to SDTM Findings-like long form.

    Motivated by the paper's Fig. 6: a checkbox CRF where each row has many
    symptom columns can be represented in SDTM as multiple records per subject
    (one record per item).

    Args:
        df: Input data.
        id_cols: Columns that identify the entity (eg, subject) to keep.
        item_cols: Wide columns to pivot. Defaults to all non-id columns.
        item_to_test: Optional mapping from wide column name -> SDTM test name.
            If provided, values will populate ``item_colname``.
        item_colname: Name of the output column holding the item/test.
        result_colname: Name of the output column holding the result/value.
        drop_missing: If True, drop rows where result is NA/blank string.

    Returns:
        A long-form dataframe with columns ``id_cols + [item_colname,
        result_colname]``.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"USUBJID": ["01-001"], "Fever": ["N"], "Chills": ["Y"]})
        >>> out = pivot_to_sdtm_findings_long(df, id_cols=["USUBJID"])
        >>> set(out["ITEM"]) == {"Fever", "Chills"}
        True
    """

    missing = [c for c in id_cols if c not in df.columns]
    if missing:
        raise ValueError(f"id_cols missing from df: {missing}")

    if item_cols is None:
        item_cols = [c for c in df.columns if c not in set(id_cols)]

    long = df.melt(
        id_vars=list(id_cols),
        value_vars=list(item_cols),
        var_name=item_colname,
        value_name=result_colname,
    )

    if item_to_test is not None:
        long[item_colname] = long[item_colname].map(item_to_test).fillna(long[item_colname])

    if drop_missing:
        v = long[result_colname]
        mask = v.notna() & ~(v.astype(str).str.strip() == "")
        long = long.loc[mask].copy()

    return long.reset_index(drop=True)
