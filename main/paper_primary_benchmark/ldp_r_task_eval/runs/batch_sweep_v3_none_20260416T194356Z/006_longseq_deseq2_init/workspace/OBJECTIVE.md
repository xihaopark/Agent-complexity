# Real R-task: longseq_deseq2_init

**Pipeline provenance:** `snakemake-workflows-rna-longseq-de-isoform` (family: `rna`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/all_counts.tsv` (first column `Reference`, one column per
sample) and `input/samples.tsv` (first column `sample`, plus `condition`).

Using DESeq2, build a DESeqDataSet from the counts matrix, use `design = ~condition`,
drop rows where total count <= 10, call `DESeq()`, and write
  - `output/dds.rds`: the DESeq2 object (saveRDS)
  - `output/normalized_counts.tsv`: columns `Reference`, then one per sample,
    `write.table(..., sep='\t', row.names=FALSE)`.

## Deliverables

- At least `output/normalized_counts.tsv` must exist when you submit.
- Full output set expected: normalized_counts.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
