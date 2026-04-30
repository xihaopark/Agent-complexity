# Real R-task: snakepipes_merge_ct

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `rna`, stage: `early`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given four Salmon quant outputs under `input/`:
`WT_A.quant.sf`, `WT_B.quant.sf`, `KO_A.quant.sf`, `KO_B.quant.sf` — tab-separated
with columns `Name, Length, EffectiveLength, TPM, NumReads`.

Merge on `Name` selecting the `TPM` column from each, using the first
dot-delimited token of the basename as the sample column name. Save the merged
matrix (with `Name` as rownames) to `output/merged_tpm.tsv` using
`write.table(..., sep='\t', quote=F, col.names=NA)`.

## Deliverables

- At least `output/merged_tpm.tsv` must exist when you submit.
- Full output set expected: merged_tpm.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
