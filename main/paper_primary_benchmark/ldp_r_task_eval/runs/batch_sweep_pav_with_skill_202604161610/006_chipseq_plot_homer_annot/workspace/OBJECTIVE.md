# Real R-task: chipseq_plot_homer_annot

**Pipeline provenance:** `snakemake-workflows-chipseq` (family: `chipseq`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given three HOMER `annotatePeaks.pl` outputs under `input/`:
`sampleA_anno.txt`, `sampleB_anno.txt`, `sampleC_anno.txt`. Each file is tab-
separated with a header that includes `Annotation`, `Distance to TSS` (renamed
`Distance.to.TSS` by R) and `Nearest PromoterID`.

Produce:
  - `output/homer_annot_summary.tsv`: a wide table (one row per sample) with the
    count of peaks per first-token feature (exon, Intergenic, intron, promoter-TSS,
    TTS, ...).
  - `output/homer_annot.pdf`: a multi-page PDF containing (1) a stacked feature-
    proportion barplot, (2) a stacked distance-bin barplot (<2kb/<5kb/<10kb/>10kb
    based on each unique gene's closest peak) and (3) a log10 violin plot of the
    `Distance.to.TSS` distribution per sample.

## Deliverables

- At least `output/homer_annot.pdf` must exist when you submit.
- Full output set expected: homer_annot.pdf, homer_annot_summary.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
