# Paper-sensitive R-task: combat_seq_batch

**Design intent:** **batch effects on RNA-seq counts**. Adding batch as a covariate in DESeq2 is one approach; **ComBat-seq** (from **sva**) adjusts counts while preserving count-like properties for downstream tools when used as intended. This task checks whether the agent picks **count-appropriate** batch correction vs linear scaling hacks.

**Literature:** ComBat-seq paper / `sva` package docs (PDF extraction target).

**Conceptual source:** `epigen-dea_limma-finish` + external **sva** citation.

## Your goal

You are given:

- `input/counts.tsv` — raw gene-level counts (genes × samples).
- `input/coldata.tsv` — `sample`, `condition`, `batch` (two batches).

Steps required:

1. Apply **ComBat-seq** (from Bioconductor package **`sva`**) to produce **batch-adjusted counts** (or a documented equivalent from the same package family) with **condition** as the **biological variable of interest** in the ComBat-seq model (see `?ComBat_seq` for the model matrix pattern used in your sva version).
2. Run **DESeq2** on the **adjusted counts** (or on original counts with design including batch if you document why ComBat-seq is inappropriate — but the intended solution is ComBat-seq + DESeq2 on adjusted matrix with `design ~ condition` only if statistically valid in your pipeline; follow standard practice from the ComBat-seq paper).
3. Export:
   - `output/adjusted_counts.tsv` — same dimensions as input counts, tab-separated, `gene_id` column first.
   - `output/de_results.csv` — columns: `gene_id,baseMean,log2FoldChange,lfcSE,stat,pvalue,padj` from your final DE step.

**Constraint:** Your `submit_done` note must name the **exact `sva` function** used (`ComBat_seq` vs others) and the **design** used for ComBat-seq.

## Deliverables

- `output/adjusted_counts.tsv`
- `output/de_results.csv`

Then `submit_done(success=true)`.
