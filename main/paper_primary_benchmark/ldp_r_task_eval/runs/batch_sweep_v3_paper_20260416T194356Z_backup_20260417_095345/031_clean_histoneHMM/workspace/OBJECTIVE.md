# Real R-task: clean_histoneHMM

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `chipseq`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given two histoneHMM filtered-regions GFFs under `input/`
(`sampleA.filtered.histoneHMM-regions.gff`, `sampleB.filtered.histoneHMM-regions.gff`),
each carrying an `avg_posterior` attribute per feature.

For each input, read with `rtracklayer::import.gff`, keep features where
`avg_posterior >= 0.5`, then:
  - write a GFF3 file to `output/<sample>_avgp0.5.gff` via `rtracklayer::export.gff3`.
  - set `score <- as.numeric(avg_posterior)` and write a BED file to
    `output/<sample>_avgp0.5.bed` via `rtracklayer::export.bed`.
Do NOT emit any image output.

## Deliverables

- At least `output/sampleA_avgp0.5.bed` must exist when you submit.
- Full output set expected: sampleA_avgp0.5.bed, sampleB_avgp0.5.bed under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
