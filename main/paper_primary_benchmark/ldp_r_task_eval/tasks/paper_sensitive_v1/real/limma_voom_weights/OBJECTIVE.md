# Paper-sensitive R-task: limma_voom_weights

**Design intent:** RNA-seq read counts with **unequal per-sample quality**; **plain `voom` + `lmFit`** is sensitive to outlier / low-complexity samples. The **limma** paper documents **`voomWithQualityWeights`** (and `arrayWeights`) to down-weight bad samples.

**Conceptual source:** `epigen-dea_limma-finish`.

## Your goal

You are given:

- `input/counts.tsv` — integer counts, first column `gene_id`, then sample columns.
- `input/coldata.tsv` — `sample`, `group` (`A` vs `B`), and `seq_depth` (library size) or similar QC covariate (see file header).

Use **limma** on voom-transformed data with **observation-level or sample-level weights**:

- You **must** use **`voomWithQualityWeights()`** (not plain `voom()`) on the DGEList or count matrix as appropriate, **or** apply `arrayWeights()` in a documented way consistent with the limma workflow for RNA-seq.
- Fit `lmFit` with `design = ~ group` and use `eBayes()`.

Export:

- `output/de_results_weighted.csv` with columns:  
  `gene_id,logFC,AveExpr,t,P.Value,adj.P.Val`

`write.csv(..., row.names=FALSE)`.

## Deliverables

- `output/de_results_weighted.csv`

Then `submit_done(success=true)`.
