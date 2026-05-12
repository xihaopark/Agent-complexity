# Real R-task: snakepipes_scrna_qc

**Pipeline provenance:** `maxplanck-ie-snakepipes-finish` (family: `scrna`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given a directory `input/qc/` containing per-library QC summaries for four
libraries across two plates:
  - `<sample>.cellsum`: tab-delimited `sample, cell_idx, READS_UNIQFEAT, UMI`
  - `<sample>.libsum`: headerless four-column table (`sample, metric, value, pct`)

Using an output prefix `output/scrna_qc`, compute:
  - `scrna_qc.libstats_reads.tsv`: per-library metrics (reads) as a wide table
  - `scrna_qc.libstats_pct.tsv`: per-library metrics (percentages) as a wide table
And render these per-plate PNGs (2 libraries per plate):
  - `scrna_qc.reads_UMI_plot.png`
  - `scrna_qc.plate_cUPM.png`
  - `scrna_qc.plate_cRPM.png`
  - `scrna_qc.plate_abs_transcripts.png`
Normalize reads/UMI per cell by per-sample sum * 1e6 before the z-score heatmap.

## Deliverables

- At least `output/scrna_qc.reads_UMI_plot.png` must exist when you submit.
- Full output set expected: scrna_qc.libstats_reads.tsv, scrna_qc.libstats_pct.tsv, scrna_qc.reads_UMI_plot.png, scrna_qc.plate_cUPM.png, scrna_qc.plate_cRPM.png, scrna_qc.plate_abs_transcripts.png under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
