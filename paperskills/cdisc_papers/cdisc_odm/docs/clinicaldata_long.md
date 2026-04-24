---
title: odm_clinicaldata_to_long
source: "Current applications and future directions for the CDISC Operational Data Model standard: A methodological review" (Hume et al., 2016)
---

# odm_clinicaldata_to_long

ODM clinical data are stored in a nested hierarchy (Fig. 3 in the paper):

`ClinicalData → SubjectData → StudyEventData → FormData → ItemGroupData → ItemData`

For analysis workflows, it is often convenient to flatten this hierarchy into a
single long table with one row per `ItemData` record.

## API

```python
from cdisc_papers.cdisc_odm import odm_clinicaldata_to_long
```

```python
odm_clinicaldata_to_long(xml: str | bytes, *, include_item_attrs: bool = True) -> pd.DataFrame
```

## Output columns

- `StudyOID`, `SubjectKey`
- `StudyEventOID`, `StudyEventRepeatKey`
- `FormOID`, `FormRepeatKey`
- `ItemGroupOID`, `ItemGroupRepeatKey`
- `ItemOID`
- If `include_item_attrs=True`: any other `ItemData` attributes such as `Value`,
  `IsNull`, `TransactionType` when present.

## Example

```python
xml = """
<ODM xmlns="http://www.cdisc.org/ns/odm/v1.3">
  <ClinicalData StudyOID="S1">
    <SubjectData SubjectKey="01-001">
      <StudyEventData StudyEventOID="SE.BASELINE" StudyEventRepeatKey="1">
        <FormData FormOID="F.DM" FormRepeatKey="1">
          <ItemGroupData ItemGroupOID="IG.DM" ItemGroupRepeatKey="1">
            <ItemData ItemOID="IT.AGE" Value="34" />
          </ItemGroupData>
        </FormData>
      </StudyEventData>
    </SubjectData>
  </ClinicalData>
</ODM>
"""

df = odm_clinicaldata_to_long(xml)
```

Then `df` contains one row with OIDs identifying the context for `IT.AGE`.
