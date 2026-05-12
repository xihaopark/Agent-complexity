---
title: pivot_to_sdtm_findings_long
source:
  document: A use-case analysis of CDISC:SDTM in academia in an investigator-initiated clinical trial.pdf
  citation: "Takahara et al. (2022) Nagoya J. Med. Sci. 84:120–132."
---

# pivot_to_sdtm_findings_long

The paper illustrates (Fig. 6) a common mismatch between paper CRFs and SDTM-style tabulation:

- **CRF / EDC wide format**: one row per subject, with one column per checkbox/item (e.g., `Fever`, `Chills`, ...).
- **SDTM Findings-like long format**: multiple rows per subject, one row per item/test, with a result/value.

`pivot_to_sdtm_findings_long()` implements this generic wide→long reshaping. While real SDTM Findings domains also include variables like `--TESTCD`, `--TEST`, `--ORRES`, and timing/visit variables, this utility provides a practical first step that can be augmented downstream.

## API

```python
pivot_to_sdtm_findings_long(
    df: pd.DataFrame,
    *,
    id_cols: Sequence[str],
    item_cols: Iterable[str] | None = None,
    item_to_test: Mapping[str, str] | None = None,
    item_colname: str = "ITEM",
    result_colname: str = "RESULT",
    drop_missing: bool = True,
) -> pd.DataFrame
```

## Examples

### 1) Pivot symptom checkboxes (Fig. 6 style)

```python
import pandas as pd
from cdisc_papers.cdisc_sdtm import pivot_to_sdtm_findings_long

wide = pd.DataFrame(
    {
        "USUBJID": ["01-001", "01-002"],
        "Fever": ["N", "Y"],
        "Chills": ["Y", "N"],
    }
)

long = pivot_to_sdtm_findings_long(wide, id_cols=["USUBJID"])
```

Output columns: `USUBJID`, `ITEM`, `RESULT`.

### 2) Map column names to standard test names

```python
long = pivot_to_sdtm_findings_long(
    wide,
    id_cols=["USUBJID"],
    item_to_test={"Fever": "FEVER", "Chills": "CHILLS"},
)
```

## Notes

- Set `drop_missing=False` if you need explicit missing rows for downstream completion checks.
- To construct SDTM-compliant variable names (e.g. `--TESTCD` restrictions), apply validation/normalization after pivoting.
