# Real R-task: chipseq_plot_peaks_count_macs2

**Pipeline provenance:** `snakemake-workflows-chipseq-finish` (family: `chipseq`, stage: `late`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given four per-sample peak-count files under `input/`
(`sampleX_control.peaks_count.txt`), each a single line `sample_control\tcount`.

Read them with `read.table(..., header=F, stringsAsFactors=F)`, rbind, and save
as a TSV at `output/peaks_count.tsv` with columns `sample_control, count`.

## Deliverables

- At least `output/peaks_count.tsv` must exist when you submit.
- Full output set expected: peaks_count.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
