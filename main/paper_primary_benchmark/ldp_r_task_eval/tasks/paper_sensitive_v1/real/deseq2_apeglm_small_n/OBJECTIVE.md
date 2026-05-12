# Paper-sensitive R-task: deseq2_apeglm_small_n

**Design intent (benchmark story):** small-sample RNA-seq differential expression where **default Wald / results() without careful shrinkage** is unstable; the DESeq2 paper recommends **`lfcShrink` with `type="apeglm"`** for low-replicate designs.

**Pipeline provenance (conceptual):** `rna-seq-star-deseq2-finish` (family: `rna`). Ground-truth scoring uses outputs produced offline from `tasks/paper_sensitive_v1/real_ground_truth/deseq2_apeglm_small_n/` and is **not** visible to the agent.

## Your goal

You are given:

- `input/counts.tsv`: gene × sample integer counts (tab-separated). First column is `gene_id`.
- `input/coldata.tsv`: rows = samples, columns include at least `sample`, `condition` (two levels: `A`, `B`). **Each group has exactly 2 replicates** (total 4 samples).

Run a DESeq2 analysis with `design = ~ condition`.

You **must** apply **effect-size shrinkage appropriate for n=2 vs n=2** using **`DESeq2::lfcShrink`** with **`type="apeglm"`** (and a valid `contrast` or `coef` — pick the coefficient corresponding to `condition` vs reference). Write **one** primary DE table:

- `output/de_results.csv` with columns **exactly**:  
  `gene_id,baseMean,log2FoldChange,lfcSE,stat,pvalue,padj`  
  Use `write.csv(..., row.names=FALSE, quote=TRUE)` or equivalent so the file is a standard CSV.

Filter out rows where `padj` is `NA` before writing (drop genes with undefined adjusted p-values).

## Notes

- Do not call `submit_done` until `output/de_results.csv` exists and is non-empty.
- If you use `results()`, follow with **`lfcShrink(dds, coef=..., type="apeglm")`** (or equivalent valid DESeq2 API) before exporting `log2FoldChange` / `lfcSE`.
- No internet; no Snakemake clusters.

## Deliverables

- `output/de_results.csv` (required)

When complete, call `submit_done(success=true)` with a one-line summary of the contrast and shrinkage method used.
