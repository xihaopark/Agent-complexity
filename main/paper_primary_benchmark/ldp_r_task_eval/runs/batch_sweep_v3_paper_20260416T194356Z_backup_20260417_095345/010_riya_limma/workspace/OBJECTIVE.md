# Real R-task: riya_limma

**Pipeline provenance:** `RiyaDua-cervical-cancer-snakemake-workflow` (family: `rna`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/exprs.csv` (pre-normalised, row = probe, column = sample)
and `input/meta.csv` with a `group` column (`cancer` vs `normal`). Use limma
(`lmFit` + `makeContrasts(cancer - normal)` + `eBayes`) to compute the top 250
DE probes (`topTable(..., adjust='fdr', number=250)`) and save to
`output/deg_results.csv` via `write.csv(...)`. Do NOT produce a volcano plot.

## Deliverables

- At least `output/deg_results.csv` must exist when you submit.
- Full output set expected: deg_results.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
