# Real R-task: methylkit_load

**Pipeline provenance:** `fritjoflammers-snakemake-methylanalysis-finish` (family: `methylation`, stage: `early`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three per-sample bismark coverage files under `input/`:
`sampleA.bismark.cov`, `sampleB.bismark.cov`, `sampleC.bismark.cov` — tab-separated
without headers, columns `(chrom, start, end, methylation_pct, count_methylated,
count_unmethylated)`.

Load them with `methylKit::methRead(..., pipeline='bismarkCoverage', mincov=4)`
using `treatment = c(0, 0, 0)` and assembly `mock_v1`, then save the resulting
methylRawList to `output/mk_raw.rds` with `saveRDS`. Use RELATIVE file paths
(`input/sampleA.bismark.cov`, ...) so the serialised object is portable. Do not
write any plot/PDF/SVG file.

## Deliverables

- At least `output/mk_raw.rds` must exist when you submit.
- Full output set expected: mk_raw.rds under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
