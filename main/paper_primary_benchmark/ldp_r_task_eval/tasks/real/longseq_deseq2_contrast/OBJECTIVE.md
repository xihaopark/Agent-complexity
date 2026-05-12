# Real R-task: longseq_deseq2_contrast

**Pipeline provenance:** `snakemake-workflows-rna-longseq-de-isoform` (family: `rna`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/dds.rds` (DESeq2 object, design=~condition, base=`wt`).
Compute `results(dds, contrast=c('condition','ko','wt'))` with `alpha=0.05`,
apply `lfcShrink(type='ashr')`, sort by padj and write a TSV to
`output/contrast_results.tsv` with columns `gene, baseMean, log2FoldChange, lfcSE,
pvalue, padj` (from `data.frame(gene=rownames(res), res)`).
Do not emit any image files — data only.

## Deliverables

- At least `output/contrast_results.tsv` must exist when you submit.
- Full output set expected: contrast_results.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
