# Real R-task: snakepipes_scrna_merge_coutt

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `scrna`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given two per-library single-cell count tables under `input/coutt/`:
`plate01_libA.corrected.txt` and `plate01_libB.corrected.txt` (tab-separated
with a `GENEID` column followed by per-cell columns `X1`..`Xn`).

Merge them by `GENEID` (outer join), prefixing each cell column with the library
name and substituting `_` for the leading `X`, and write:
  - `output/merged_coutt.tsv`: the merged GENEID × cells table (tab-sep,
    `write.table(..., sep='\t', col.names=T, quote=F, row.names=F)`).
  - `output/merged_coutt.cell_names.tsv`: a cell manifest with columns
    `sample, plate, library, cell_idx, cell_name` (tab-sep).

## Deliverables

- At least `output/merged_coutt.tsv` must exist when you submit.
- Full output set expected: merged_coutt.tsv, merged_coutt.cell_names.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
