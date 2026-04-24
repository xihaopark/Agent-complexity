# Paper-sensitive R-task: limma_duplicatecorrelation

**Design intent:** **paired** or **repeated-measure** designs; the correct **limma** pattern is often **`duplicateCorrelation`** to estimate a **block** correlation, then `lmFit` with `block` + `correlation=`.

**Conceptual source:** `epigen-dea_limma-finish`.

## Your goal

You are given:

- `input/counts.tsv` — RNA-seq counts.
- `input/coldata.tsv` — includes `sample`, `patient` (block), and `treatment` (two levels).

You must use **limma** with **duplicate correlation**:

- `design <- model.matrix(~treatment, data=...)`
- `cor <- duplicateCorrelation(y, design, block=patient_vector)$consensus` (or equivalent from the `limma` API for your DGE/ExpressionSet setup)
- `fit <- lmFit(y, design, block=..., correlation=cor)` then `eBayes()`

Export `output/paired_de.csv` with columns: `gene_id,logFC,t,P.Value,adj.P.Val`

## Deliverables

- `output/paired_de.csv`

Then `submit_done(success=true)`.
