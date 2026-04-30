import pandas as pd
import pytest

from cdisc_papers.cdisc_sdtm import pivot_to_sdtm_findings_long


def test_pivot_to_sdtm_findings_long_basic_and_drop_missing():
    df = pd.DataFrame(
        {
            "USUBJID": ["01-001", "01-002"],
            "Fever": ["N", ""],
            "Chills": ["Y", None],
        }
    )
    out = pivot_to_sdtm_findings_long(df, id_cols=["USUBJID"])

    # 2 subjects * 2 items = 4 rows originally, but subject 2 has missing/blank.
    assert out.shape[0] == 2
    assert set(out.columns) == {"USUBJID", "ITEM", "RESULT"}
    assert set(out["ITEM"]) == {"Fever", "Chills"}


def test_pivot_to_sdtm_findings_long_mapping_and_keep_missing():
    df = pd.DataFrame({"USUBJID": ["01-001"], "Fever": ["N"]})
    out = pivot_to_sdtm_findings_long(
        df,
        id_cols=["USUBJID"],
        item_to_test={"Fever": "SYMPTOM"},
        drop_missing=False,
    )
    assert out.loc[0, "ITEM"] == "SYMPTOM"
    assert out.loc[0, "RESULT"] == "N"


def test_pivot_to_sdtm_findings_long_missing_id_cols_raises():
    df = pd.DataFrame({"SUBJID": ["01-001"], "Fever": ["N"]})
    with pytest.raises(ValueError, match="id_cols missing"):
        pivot_to_sdtm_findings_long(df, id_cols=["USUBJID"])
