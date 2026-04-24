# Real R-task: spilterlize_norm_voom

**Pipeline provenance:** `epigen-spilterlize_integrate-finish` (family: `rna`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/filtered_counts.csv` (first column row-name = gene, other
columns samples). Run `edgeR::DGEList` → `calcNormFactors(method='TMM')` →
`limma::voom(normalize.method='none', span=0.5, plot=TRUE)` and write the
resulting `voom_results$E` matrix to `output/normalized_counts.csv` via
`data.table::fwrite(..., row.names=TRUE)`. Do not persist any image file.

## Deliverables

- At least `output/normalized_counts.csv` must exist when you submit.
- Full output set expected: normalized_counts.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
