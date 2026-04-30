import pandas as pd

from cdisc_papers.cdisc_odm import odm_clinicaldata_to_long


def test_clinicaldata_to_long_parses_minimal_hierarchy_with_namespace():
    xml = """
    <ODM xmlns="http://www.cdisc.org/ns/odm/v1.3">
      <ClinicalData StudyOID="S1">
        <SubjectData SubjectKey="SUBJ1">
          <StudyEventData StudyEventOID="SE1" StudyEventRepeatKey="1">
            <FormData FormOID="F1" FormRepeatKey="1">
              <ItemGroupData ItemGroupOID="IG1" ItemGroupRepeatKey="1">
                <ItemData ItemOID="IT.AGE" Value="34" TransactionType="Insert" />
              </ItemGroupData>
            </FormData>
          </StudyEventData>
        </SubjectData>
      </ClinicalData>
    </ODM>
    """

    out = odm_clinicaldata_to_long(xml)
    assert len(out) == 1
    assert out.loc[0, "StudyOID"] == "S1"
    assert out.loc[0, "SubjectKey"] == "SUBJ1"
    assert out.loc[0, "StudyEventOID"] == "SE1"
    assert out.loc[0, "ItemOID"] == "IT.AGE"
    assert out.loc[0, "Value"] == "34"
    assert out.loc[0, "TransactionType"] == "Insert"


def test_clinicaldata_to_long_include_item_attrs_false_only_value():
    xml = """
    <ODM xmlns="http://www.cdisc.org/ns/odm/v1.3">
      <ClinicalData StudyOID="S1">
        <SubjectData SubjectKey="SUBJ1">
          <StudyEventData StudyEventOID="SE1">
            <FormData FormOID="F1">
              <ItemGroupData ItemGroupOID="IG1">
                <ItemData ItemOID="IT.AGE" Value="34" TransactionType="Insert" />
              </ItemGroupData>
            </FormData>
          </StudyEventData>
        </SubjectData>
      </ClinicalData>
    </ODM>
    """

    out = odm_clinicaldata_to_long(xml, include_item_attrs=False)
    assert list(out.columns).count("Value") == 1
    assert "TransactionType" not in out.columns
    assert out.loc[0, "Value"] == "34"


def test_clinicaldata_to_long_handles_multiple_items():
    xml = """
    <ODM xmlns="http://www.cdisc.org/ns/odm/v1.3">
      <ClinicalData StudyOID="S1">
        <SubjectData SubjectKey="SUBJ1">
          <StudyEventData StudyEventOID="SE1">
            <FormData FormOID="F1">
              <ItemGroupData ItemGroupOID="IG1">
                <ItemData ItemOID="IT.AGE" Value="34" />
                <ItemData ItemOID="IT.SEX" Value="M" />
              </ItemGroupData>
            </FormData>
          </StudyEventData>
        </SubjectData>
      </ClinicalData>
    </ODM>
    """

    out = odm_clinicaldata_to_long(xml)
    assert set(out["ItemOID"]) == {"IT.AGE", "IT.SEX"}
    assert pd.api.types.is_object_dtype(out["Value"])
