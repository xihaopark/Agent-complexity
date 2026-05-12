from __future__ import annotations

from typing import Any
import xml.etree.ElementTree as ET

import pandas as pd

from ._xml_utils import findall_local


def odm_metadata_to_tables(xml: str | bytes) -> dict[str, pd.DataFrame]:
    """Extract key ODM metadata objects into pandas DataFrames.

    This is a lightweight parser meant to support joining clinical data
    (``ItemOID``) to human-readable labels and structural context.

    Captures the most common definitions from ``MetaDataVersion``:
    ``StudyEventDef``, ``FormDef``, ``ItemGroupDef``, and ``ItemDef``.

    Args:
        xml: ODM XML content (string or bytes).

    Returns:
        Dict of tables. Keys include: ``study_event_def``, ``form_def``,
        ``itemgroup_def``, ``item_def``. Each table includes the ``OID`` and
        selected attributes like ``Name`` and ``Repeating``.

    Example:
        >>> xml = """<ODM xmlns='http://www.cdisc.org/ns/odm/v1.3'>\
        ... <Study OID='S1'><MetaDataVersion OID='MDV1'>\
        ...  <ItemDef OID='IT.AGE' Name='Age' DataType='integer'/>\
        ... </MetaDataVersion></Study></ODM>"""
        >>> tables = odm_metadata_to_tables(xml)
        >>> tables['item_def'].loc[0, 'OID']
        'IT.AGE'
    """

    root = ET.fromstring(xml)

    def _table(tag: str, *, keep: tuple[str, ...]) -> pd.DataFrame:
        recs: list[dict[str, Any]] = []
        for e in findall_local(root, tag):
            r = {k: e.attrib.get(k) for k in keep if k in e.attrib or k == keep[0]}
            # ensure first key exists even if missing
            if keep[0] not in r:
                r[keep[0]] = e.attrib.get(keep[0])
            recs.append(r)
        return pd.DataFrame.from_records(recs)

    return {
        "study_event_def": _table(
            "StudyEventDef", keep=("OID", "Name", "Repeating", "Type")
        ),
        "form_def": _table("FormDef", keep=("OID", "Name", "Repeating")),
        "itemgroup_def": _table(
            "ItemGroupDef", keep=("OID", "Name", "Repeating", "SASDatasetName")
        ),
        "item_def": _table(
            "ItemDef", keep=("OID", "Name", "DataType", "Length", "CodeListOID")
        ),
    }
