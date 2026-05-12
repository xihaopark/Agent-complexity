from __future__ import annotations

import xml.etree.ElementTree as ET

import pandas as pd

from ._clinicaldata_parse import iter_clinicaldata_item_rows


def odm_clinicaldata_to_long(
    xml: str | bytes,
    *,
    include_item_attrs: bool = True,
) -> pd.DataFrame:
    """Parse ODM ``ClinicalData`` into a tidy long dataframe.

    ODM represents clinical data hierarchically (SubjectData → StudyEventData →
    FormData → ItemGroupData → ItemData). This function flattens that hierarchy
    into one row per ``ItemData``.

    Args:
        xml: ODM XML content (string or bytes).
        include_item_attrs: If True, include ``ItemData`` attributes (eg,
            ``Value``, ``IsNull``, ``TransactionType``) as columns.

    Returns:
        Long-form dataframe with columns for OIDs at each level plus item value.

    Example:
        >>> xml = """<ODM xmlns='http://www.cdisc.org/ns/odm/v1.3'>\
        ... <ClinicalData StudyOID='S1'>\
        ...  <SubjectData SubjectKey='SUBJ1'>\
        ...   <StudyEventData StudyEventOID='SE1'>\
        ...    <FormData FormOID='F1'>\
        ...     <ItemGroupData ItemGroupOID='IG1'>\
        ...      <ItemData ItemOID='IT.AGE' Value='34'/>\
        ...     </ItemGroupData></FormData></StudyEventData></SubjectData>\
        ... </ClinicalData></ODM>"""
        >>> df = odm_clinicaldata_to_long(xml)
        >>> df.loc[0, 'ItemOID']
        'IT.AGE'
    """

    root = ET.fromstring(xml)
    rows = iter_clinicaldata_item_rows(root, include_item_attrs=include_item_attrs)
    return pd.DataFrame.from_records(rows)
