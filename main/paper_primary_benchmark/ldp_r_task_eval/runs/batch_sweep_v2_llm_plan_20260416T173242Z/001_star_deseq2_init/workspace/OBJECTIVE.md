# Real R-task: star_deseq2_init

**Pipeline provenance:** `rna-seq-star-deseq2-finish` (family: `rna`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given:
  - `input/counts.tsv`: a tab-delimited count matrix with a first column `gene`
    followed by one column per sample (A1, A2, A3, B1, B2, B3).
  - `input/samples.tsv`: a samples sheet with columns `sample_name` and `condition`
    where `A*` rows are `treated` and `B*` rows are `untreated`.

Using DESeq2, build a DESeqDataSet from the count matrix with `design = ~condition`
and the `untreated` level relevelled as the base. Call `DESeq()` on it. Write:
  - `output/dds.rds`: the DESeq2 object produced by `saveRDS(dds, ...)`.
  - `output/normalized_counts.tsv`: a tab-delimited table with a first column `gene`
    and one column per sample of DESeq2 normalised counts, written with
    `write.table(..., sep='\t', row.names=FALSE)`.
Drop rows whose total count <= 1 before running DESeq.

## Deliverables

- At least `output/normalized_counts.tsv` must exist when you submit.
- Full output set expected: normalized_counts.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
