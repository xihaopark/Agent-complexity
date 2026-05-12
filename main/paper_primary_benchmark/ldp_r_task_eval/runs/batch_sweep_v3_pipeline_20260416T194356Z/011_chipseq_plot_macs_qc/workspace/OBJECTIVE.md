# Real R-task: chipseq_plot_macs_qc

**Pipeline provenance:** `snakemake-workflows-chipseq-finish` (family: `chipseq`, stage: `late`, difficulty: `2`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three narrowPeak files under `input/`: `sampleA_peaks.narrowPeak`,
`sampleB_peaks.narrowPeak`, `sampleC_peaks.narrowPeak` (tab-separated, 10-col
MACS2 narrowPeak schema).

For each sample compute summary statistics on `fold`, `-log10(qvalue)`,
`-log10(pvalue)` and peak `length`, producing rows of Min/1st Qu/Median/Mean/3rd
Qu/Max plus `num_peaks`, `measure`, `sample`. Save the combined table to
`output/macs_qc_summary.tsv` via
`write.table(summary.dat, sep='\t', row.names=FALSE, col.names=TRUE, quote=FALSE)`.
Do not emit a PDF plot.

## Deliverables

- At least `output/macs_qc_summary.tsv` must exist when you submit.
- Full output set expected: macs_qc_summary.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
