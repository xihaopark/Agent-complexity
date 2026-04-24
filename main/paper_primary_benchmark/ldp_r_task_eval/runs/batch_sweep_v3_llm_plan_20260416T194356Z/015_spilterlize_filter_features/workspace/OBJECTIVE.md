# Real R-task: spilterlize_filter_features

**Pipeline provenance:** `epigen-spilterlize_integrate-finish` (family: `rna`, stage: `early`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/counts.csv` (first column is the row-name for genes; other
columns are samples) and `input/annotation.csv` (first column row-name = sample,
columns `group, batch`). Filter features using `edgeR::filterByExpr` with
`group = annot$group` and write the filtered matrix to
`output/filtered_counts.csv` via `data.table::fwrite(..., row.names=TRUE)`.

## Deliverables

- At least `output/filtered_counts.csv` must exist when you submit.
- Full output set expected: filtered_counts.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
