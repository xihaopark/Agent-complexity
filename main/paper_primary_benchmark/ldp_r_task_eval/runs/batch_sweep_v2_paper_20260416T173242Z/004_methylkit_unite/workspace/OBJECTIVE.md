# Real R-task: methylkit_unite

**Pipeline provenance:** `fritjoflammers-snakemake-methylanalysis-finish` (family: `methylation`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given four per-sample bismark-style coverage files under `input/`:
`sampleA.bismark.cov`, `sampleB.bismark.cov`, `sampleC.bismark.cov`,
`sampleD.bismark.cov` — tab-separated without headers, columns
`(chrom, start, end, methylation_pct, count_methylated, count_unmethylated)`.

Load them with `methylKit::methRead(..., pipeline='bismarkCoverage', mincov=4)`,
using `treatment = c(0, 0, 1, 1)` and assembly `mock_v1`. Then run
`methylKit::unite(mk_raw, min.per.group=1, destrand=FALSE)` and save:
  - `output/mk_united.rds`: the united methylBase object (`saveRDS`).
  - `output/unite_stats.tsv`: a single-row tab-separated table with columns
    `n_samples, n_sites, min_per_group, destrand, use_db, db_path` (`write_tsv`).

## Deliverables

- At least `output/unite_stats.tsv` must exist when you submit.
- Full output set expected: unite_stats.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
