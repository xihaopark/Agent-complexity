# Real R-task: spilterlize_norm_edger

**Pipeline provenance:** `epigen-spilterlize_integrate-finish` (family: `rna`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/filtered_counts.csv` (gene × sample). Run
`edgeR::DGEList` → `calcNormFactors(method='TMM')` → `cpm(log=TRUE,
prior.count=3)` and save the log-CPM matrix to `output/all/normTMM.csv` via
`data.table::fwrite(..., row.names=TRUE)`.

## Deliverables

- At least `output/all/normTMM.csv` must exist when you submit.
- Full output set expected: all/normTMM.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
