# Real R-task: dea_limma

**Pipeline provenance:** `epigen-dea_limma-finish` (family: `rna`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/counts.tsv` (gene × sample) and `input/metadata.tsv`
(first column sample_name, plus a `treatment` column with `UT`/`TR`). Run the
epigen `dea_limma` pipeline (design=`~treatment`, TMM + voom + eBayes) and write:
  - `output/dea_results.csv` with columns `feature, logFC, AveExpr, t, P.Value,
    adj.P.Val, B, group` (fwrite).
  - `output/lmfit.rds` (fitted limma `lmFit` object, via `saveRDS`).
  - `output/model_matrix.csv` (fwrite with row.names=TRUE).
Do not persist any image output.

## Deliverables

- At least `output/dea_results.csv` must exist when you submit.
- Full output set expected: dea_results.csv, model_matrix.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
