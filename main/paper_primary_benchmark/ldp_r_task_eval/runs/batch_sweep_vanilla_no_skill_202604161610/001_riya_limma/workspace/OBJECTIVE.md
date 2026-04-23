# Real R-task: riya_limma

**Pipeline provenance:** `RiyaDua-cervical-cancer-snakemake-workflow` (family: `rna`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given:
  - `input/expression.csv`: expression matrix (genes x samples; first column = gene id).
  - `input/metadata.csv`: sample metadata with a `group` column (`normal` vs `cancer`).

Using the limma pipeline (lmFit + contrasts `cancer - normal` + eBayes), compute the top
250 differentially expressed genes and write them (csv) to `output/deg_results.csv`.
Use `write.csv(deg_results, 'output/deg_results.csv')` so the first column is the gene id.

## Deliverables

- At least `output/deg_results.csv` must exist when you submit.
- Full output set expected: deg_results.csv, volcano.png under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
