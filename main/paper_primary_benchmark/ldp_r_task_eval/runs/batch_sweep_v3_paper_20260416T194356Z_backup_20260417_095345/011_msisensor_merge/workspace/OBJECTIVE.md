# Real R-task: msisensor_merge

**Pipeline provenance:** `snakemake-workflows-msisensor-pro-finish` (family: `variant`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given multiple MSIsensor outputs at
`results/msi/<sample>/msi_out.txt` (tab-separated with header:
`Total_Number_of_Sites, Number_of_Unstable_Sites, %`). Read all of them, tag
each row with a `group` column extracted from the path (second path component
after `results/`), rename `Total_Number_of_Sites -> n_all_sites`,
`Number_of_Unstable_Sites -> n_unstable_sites`, `% -> msi_score`, and write
to `output/merged_msi.tsv` via `readr::write_tsv`.

## Deliverables

- At least `output/merged_msi.tsv` must exist when you submit.
- Full output set expected: merged_msi.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
