# Real R-task: methylkit_to_tibble

**Pipeline provenance:** `fritjoflammers-snakemake-methylanalysis-finish` (family: `methylation`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given a methylKit united object at `input/mk_united.rds`. Convert it into
a long tibble with columns `(chr, start, end, strand, metric, value, sample)` using
`pivot_longer` on the `coverage*`/`numCs*` columns, and save it to
`output/df_mku.rds`. Then pivot wide on `metric`, compute `mCpG = numCs / coverage`,
group by `(sample, chr)`, and write the mean mCpG table to `output/mean_mcpg.tsv`
using `readr::write_tsv` with columns `sample, chr, mean_mCpG`.

## Deliverables

- At least `output/mean_mcpg.tsv` must exist when you submit.
- Full output set expected: mean_mcpg.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
