# Real R-task: epigenbutton_peak_stats

**Pipeline provenance:** `joncahn-epigeneticbutton` (family: `chipseq`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/peak_stats.tsv`, a tab-separated peak summary with columns
`Line, Tissue, Sample, Selected_peaks, Peaks_in_Rep1, Peaks_in_Rep2,
Peaks_in_merged, Peaks_in_pseudo_reps, Peaks_in_idr`. `Selected_peaks` is formatted
as `<count> selected`; strip to the numeric prefix.

Render `output/peak_stats.pdf` (10x12 in) with a grouped barplot faceted on
`Line + Tissue`, showing the number of peaks per sample at each stage
(Rep1, Rep2, Merged, Pseudoreps, IDR, Selected) using the Paired palette.
Title: `Number of peaks in each ChIP sample of ChIP_demo`.

## Deliverables

- At least `output/peak_stats.pdf` must exist when you submit.
- Full output set expected: peak_stats.pdf under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
