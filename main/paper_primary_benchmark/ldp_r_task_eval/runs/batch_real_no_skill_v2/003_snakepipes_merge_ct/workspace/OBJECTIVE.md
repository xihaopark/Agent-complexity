# Real R-task: snakepipes_merge_ct

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `rna`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three Salmon-style quant files under `input/` named
`sampleA.quant.sf`, `sampleB.quant.sf`, `sampleC.quant.sf` with columns
`Name, Length, EffectiveLength, TPM, NumReads`.

For each file, keep only (`Name`, `TPM`) and rename the TPM column to the sample
basename (everything before the first `.`). Outer-merge all three files by `Name`.
Write the merged table to `output/merged_tpm.tsv` using tab separators with
`quote=FALSE`, `col.names=NA`, rownames = Name, and drop the explicit `Name` column.

## Deliverables

- At least `output/merged_tpm.tsv` must exist when you submit.
- Full output set expected: merged_tpm.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
