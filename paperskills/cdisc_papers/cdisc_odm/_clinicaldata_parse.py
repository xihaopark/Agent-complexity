from __future__ import annotations

from typing import Any
import xml.etree.ElementTree as ET

from ._xml_utils import local_name


def iter_clinicaldata_item_rows(root: ET.Element, *, include_item_attrs: bool) -> list[dict[str, Any]]:
    """Return list of dict rows, one per ItemData, from an ODM XML root."""

    rows: list[dict[str, Any]] = []
    for cd in root.iter():
        if local_name(cd.tag) != "ClinicalData":
            continue
        base_cd = {"StudyOID": cd.attrib.get("StudyOID")}
        for subj in cd:
            if local_name(subj.tag) != "SubjectData":
                continue
            base_subj = base_cd | {"SubjectKey": subj.attrib.get("SubjectKey")}
            for se in subj:
                if local_name(se.tag) != "StudyEventData":
                    continue
                base_se = base_subj | {
                    "StudyEventOID": se.attrib.get("StudyEventOID"),
                    "StudyEventRepeatKey": se.attrib.get("StudyEventRepeatKey"),
                }
                for form in se:
                    if local_name(form.tag) != "FormData":
                        continue
                    base_form = base_se | {
                        "FormOID": form.attrib.get("FormOID"),
                        "FormRepeatKey": form.attrib.get("FormRepeatKey"),
                    }
                    for ig in form:
                        if local_name(ig.tag) != "ItemGroupData":
                            continue
                        base_ig = base_form | {
                            "ItemGroupOID": ig.attrib.get("ItemGroupOID"),
                            "ItemGroupRepeatKey": ig.attrib.get("ItemGroupRepeatKey"),
                        }
                        for item in ig:
                            if local_name(item.tag) != "ItemData":
                                continue
                            row = base_ig | {"ItemOID": item.attrib.get("ItemOID")}
                            if include_item_attrs:
                                for k, v in item.attrib.items():
                                    if k != "ItemOID":
                                        row[k] = v
                            else:
                                row["Value"] = item.attrib.get("Value")
                            rows.append(row)
    return rows
