---
title: odm_metadata_to_tables
source: "Current applications and future directions for the CDISC Operational Data Model standard: A methodological review" (Hume et al., 2016)
---

# odm_metadata_to_tables

ODM separates **metadata** (study structure, item definitions) from **clinical
instance data**.

When you flatten `ClinicalData` to long form, you typically want to join the
`ItemOID` values to their human-readable names and attributes from the
`MetaDataVersion` section.

## API

```python
from cdisc_papers.cdisc_odm import odm_metadata_to_tables
```

```python
odm_metadata_to_tables(xml: str | bytes) -> dict[str, pd.DataFrame]
```

## Returned tables

The function returns a dictionary of DataFrames:

- `study_event_def`: rows from `StudyEventDef`
- `form_def`: rows from `FormDef`
- `itemgroup_def`: rows from `ItemGroupDef`
- `item_def`: rows from `ItemDef`

Each table includes the `OID` column plus common attributes like `Name` and
`Repeating` when present.

## Example: join ItemOID to Item name

```python
from cdisc_papers.cdisc_odm import odm_clinicaldata_to_long, odm_metadata_to_tables

long = odm_clinicaldata_to_long(odm_xml)
meta = odm_metadata_to_tables(odm_xml)

long_named = long.merge(
    meta["item_def"].rename(columns={"OID": "ItemOID", "Name": "ItemName"}),
    on="ItemOID",
    how="left",
)
```
