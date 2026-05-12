# Real R-task: methylkit_filt_norm

**Pipeline provenance:** `fritjoflammers-snakemake-methylanalysis-finish` (family: `methylation`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/mk_raw.rds` (methylRawList, methylKit). Apply
`filterByCoverage(lo.count=3, hi.perc=99.9)` then
`normalizeCoverage(method='median')`; save the normalized object to
`output/mk_filt_norm.rds` and write a per-sample stats TSV to
`output/filt_norm_stats.tsv` (columns `sample, n_CpGs, mean_mCpG,
mean_coverage, median_coverage`).

## Deliverables

- At least `output/filt_norm_stats.tsv` must exist when you submit.
- Full output set expected: filt_norm_stats.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
