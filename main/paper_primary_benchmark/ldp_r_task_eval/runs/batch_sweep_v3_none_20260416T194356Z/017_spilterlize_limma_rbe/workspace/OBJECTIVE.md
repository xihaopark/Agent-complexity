# Real R-task: spilterlize_limma_rbe

**Pipeline provenance:** `epigen-spilterlize_integrate-finish` (family: `rna`, stage: `late`, difficulty: `3`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/normalized.csv` (gene × sample log-scale data) and
`input/annotation.csv` (sample × `group, batch`). Call
`limma::removeBatchEffect(as.matrix(data), batch=annot$batch,
design=model.matrix(~group, annot))` and write to
`output/integrated_data.csv` via `data.table::fwrite(..., row.names=TRUE)`.

## Deliverables

- At least `output/integrated_data.csv` must exist when you submit.
- Full output set expected: integrated_data.csv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
