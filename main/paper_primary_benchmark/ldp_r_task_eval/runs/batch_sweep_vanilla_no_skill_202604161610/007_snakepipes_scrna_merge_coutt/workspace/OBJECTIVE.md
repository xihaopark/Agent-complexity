# Real R-task: snakepipes_scrna_merge_coutt

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `scrna`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given a directory `input/coutt/` containing three per-library
`*.corrected.txt` files (`plate1_lib1`, `plate1_lib2`, `plate2_lib1`). Each file
has a `GENEID` column followed by per-cell columns named `X1..X8`.

Merge the tables by `GENEID` using an outer join, prefixing each original column
name with the source basename (e.g. `plate1_lib1_1`, `plate1_lib1_2`, ...), and
replace NA counts with 0.

Write two outputs:
  - `output/merged_coutt.tsv`: tab-delimited merged count matrix.
  - `output/merged_coutt.cell_names.tsv`: five-column table (`sample, plate,
    library, cell_idx, cell_name`) where plate/library are inferred from library
    order (2 libraries per plate).

## Deliverables

- At least `output/merged_coutt.tsv` must exist when you submit.
- Full output set expected: merged_coutt.tsv, merged_coutt.cell_names.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
