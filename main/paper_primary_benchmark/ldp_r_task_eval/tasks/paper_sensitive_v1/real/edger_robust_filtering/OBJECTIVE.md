# Paper-sensitive R-task: edger_robust_filtering

**Design intent:** **edgeR** `glmQLFit` supports **`robust=TRUE`** to limit outlier impact; also `filterByExpr` for low counts. Naive pipelines may skip robustness.

**Conceptual source:** `epigen-rnaseq_pipeline-finish`.

## Your goal

You are given:

- `input/counts.tsv` — integer counts.
- `input/coldata.tsv` — `sample`, `group` (two groups), and an optional column `is_outlier` (0/1) — one sample may be flagged (synthetic).

Run a **QLF-style** edgeR analysis:

- Build DGEList, `calcNormFactors`, `estimateDisp`, then **`glmQLFit(..., robust=TRUE)`** and **`glmQLFTest`**.
- Export `output/de_robust.tsv` with columns: `gene_id,logFC,logCPM,F,PValue,FDR`

## Deliverables

- `output/de_robust.tsv`

Then `submit_done(success=true)`.
