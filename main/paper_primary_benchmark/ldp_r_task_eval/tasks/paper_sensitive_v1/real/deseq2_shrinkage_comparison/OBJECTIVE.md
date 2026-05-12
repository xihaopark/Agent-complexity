# Paper-sensitive R-task: deseq2_shrinkage_comparison

**Design intent:** `lfcShrink` **type** options (`apeglm`, `ashr`, `normal`, …) have different **behavior and defaults**. The DESeq2 paper discusses shrinkage; agents often pick deprecated types or inconsistent contrasts.

**Conceptual source:** `rna-seq-star-deseq2-finish`.

## Your goal

You are given:

- `input/counts.tsv` — at least 6 samples (3 vs 3).
- `input/coldata.tsv` — `sample`, `condition` (`A`,`B`).

Run `DESeq()` then produce **one** final DE table using **`lfcShrink` with `type="apeglm"`** as the **primary** reported shrunk coefficients (even if you compare internally with `ashr`).

- `output/shrunk_de.csv` — columns: `gene_id,baseMean,log2FoldChange,lfcSE,stat,pvalue,padj`  
  where `log2FoldChange` and `lfcSE` are from the **apeglm**-shrunk `results` object when available.

**Constraint:** in `submit_done`, list the **`coef` name** and confirm **`type="apeglm"`**.

## Deliverables

- `output/shrunk_de.csv`

Then `submit_done(success=true)`.
