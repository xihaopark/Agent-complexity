# Real R-task: snakepipes_scrna_qc

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `scrna`, stage: `mid`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given per-library `.cellsum` (header: `sample, cell_idx,
READS_UNIQFEAT, UMI`) and `.libsum` (no header; 4 cols: sample, metric,
reads, pct) files under `input/cellsum/`.

For every `.libsum`, dcast on `sample × metric` using `value.var='V3'` (→
`scqc.libstats_reads.tsv`) and `value.var='V4'` (→ `scqc.libstats_pct.tsv`).
Write both with `sep='\t', row.names=F, quote=F`. Produce NO plot files.

## Deliverables

- At least `output/scqc.libstats_reads.tsv` must exist when you submit.
- Full output set expected: scqc.libstats_reads.tsv, scqc.libstats_pct.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
