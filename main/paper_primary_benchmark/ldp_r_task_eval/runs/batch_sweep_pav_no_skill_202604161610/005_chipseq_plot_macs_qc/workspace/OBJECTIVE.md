# Real R-task: chipseq_plot_macs_qc

**Pipeline provenance:** `snakemake-workflows-chipseq` (family: `chipseq`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three MACS2-style narrowPeak BED files under `input/`:
  - `sampleA_peaks.narrowPeak`
  - `sampleB_peaks.narrowPeak`
  - `sampleC_peaks.narrowPeak`

Each file has 10 tab-delimited columns (chrom, start, end, name, pileup, strand,
fold, -log10(pvalue), -log10(qvalue), summit).

Produce two files under `output/`:
  - `macs_qc_summary.tsv`: per-sample summary statistics (Min/1stQu/Median/Mean/
    3rdQu/Max plus `num_peaks`, `measure`, `sample`) for `fold`, `-log10(qvalue)`,
    `-log10(pvalue)`, and `length` (end-start).
  - `macs_qc.pdf`: a multi-page PDF with the peak count barplot and three violin
    plots (length on log10, fold on log2, FDR / pvalue on linear -log10).

## Deliverables

- At least `output/macs_qc.pdf` must exist when you submit.
- Full output set expected: macs_qc.pdf, macs_qc_summary.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
