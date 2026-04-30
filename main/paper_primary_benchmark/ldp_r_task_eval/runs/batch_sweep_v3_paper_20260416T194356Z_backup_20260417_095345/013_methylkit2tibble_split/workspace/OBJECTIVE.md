# Real R-task: methylkit2tibble_split

**Pipeline provenance:** `fritjoflammers-snakemake-methylanalysis-finish` (family: `methylation`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given a list of per-group tibble RDS files in
`snakemake@input$rds_list` (each containing a `mku2tibble`-style long-format
tibble with columns `chr, start, ..., metric, value, sample`). Concatenate them
and save to `output/df_mku_split.rds`. Then pivot wider on `metric`, compute
`mCpG = numCs / coverage` (dropping `coverage==0`), group by `(sample, chr)`
and write the mean mCpG per group to `output/mean_mcpg_split.tsv` via
`readr::write_tsv`.

## Deliverables

- At least `output/mean_mcpg_split.tsv` must exist when you submit.
- Full output set expected: mean_mcpg_split.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
