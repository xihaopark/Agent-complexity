# Real R-task: snakepipes_scrna_report

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `scrna`, stage: `late`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three single-library metric CSV files under `input/` named
`libA.metrics.csv`, `libB.metrics.csv`, `libC.metrics.csv` (no header; two
columns `Metric,<value>`). Each library omits a different Metric row to
exercise outer-merge semantics.

Read each file with `read.table(..., header=FALSE, sep=',', as.is=TRUE)`,
rename columns to `Metric, <libID>` and merge them via `Reduce(function(x,y)
merge(x,y,all=TRUE,by='Metric',sort=FALSE), ...)`. Write the merged table
to `output/scrna_report.tsv` via `write.table(..., row.names=FALSE,
quote=FALSE, sep='\t')`.

## Deliverables

- At least `output/scrna_report.tsv` must exist when you submit.
- Full output set expected: scrna_report.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
