# Real R-task: star_deseq2_contrast

**Pipeline provenance:** `rna-seq-star-deseq2-finish` (family: `rna`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/dds.rds`, a pre-built DESeq2 object (design = ~condition)
with treated/untreated samples. The base level is `untreated`.

Using DESeq2, compute results for the contrast `condition treated vs untreated`,
apply `lfcShrink(type='ashr')`, sort by padj and write a tab-delimited table to
`output/contrast_results.tsv` whose columns are `gene, baseMean, log2FoldChange,
lfcSE, pvalue, padj` (as produced by `data.frame(gene=rownames(res), res)` followed
by `write.table(..., sep='\t', row.names=FALSE)`).
Do NOT emit any image file — data only.

## Deliverables

- At least `output/contrast_results.tsv` must exist when you submit.
- Full output set expected: contrast_results.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
