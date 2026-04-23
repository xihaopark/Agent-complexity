# Real R-task: phantompeak_correlation

**Pipeline provenance:** `snakemake-workflows-chipseq-finish` (family: `chipseq`, stage: `late`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/header.csv` (single line `shift,cross_correlation`) and
`input/run_spp.RData` (contains a `crosscorr` list with data.frame slot
`cross.correlation` of shift / correlation values). Copy the header to
`output/crosscorr.csv`, then append the `crosscorr$cross.correlation`
data.frame values (no header, no rownames, comma-separated).

## Deliverables

- At least `output/crosscorr.csv` must exist when you submit.
- Full output set expected: crosscorr.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
