# Real R-task: methylkit_remove_snvs

**Pipeline provenance:** `fritjoflammers-snakemake-methylanalysis-finish` (family: `methylation`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/df_united.rds` (a long-format methylKit tibble) and
`input/exclusion.bed` (TSV: seqnames start end ref alt score). Anti-join the
tibble against the bed (converting `start` to 1-based by `start + 1`), save the
filtered tibble to `output/df_united_excl.rds`, and write a summary TSV at
`output/snv_stats.tsv` with columns `dataset, n_sites` and rows `united` /
`united_excl`.

## Deliverables

- At least `output/snv_stats.tsv` must exist when you submit.
- Full output set expected: snv_stats.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
