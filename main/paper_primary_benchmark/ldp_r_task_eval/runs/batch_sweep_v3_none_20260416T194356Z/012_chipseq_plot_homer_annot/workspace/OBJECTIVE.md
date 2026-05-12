# Real R-task: chipseq_plot_homer_annot

**Pipeline provenance:** `snakemake-workflows-chipseq-finish` (family: `chipseq`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three HOMER annotatePeaks outputs under `input/`: `sampleA_annot.txt`,
`sampleB_annot.txt`, `sampleC_annot.txt` (tab-separated, HOMER schema). For each
sample, aggregate feature counts by the first whitespace token of `Annotation`,
then cast to a wide matrix (`sample` x feature). Save to
`output/homer_annot_summary.tsv` via `write.table(..., sep='\t', row.names=F,
col.names=T, quote=F)`. Do not emit any PDF plot.

## Deliverables

- At least `output/homer_annot_summary.tsv` must exist when you submit.
- Full output set expected: homer_annot_summary.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
