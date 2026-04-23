# Real R-task: chipseq_plot_annotatepeaks_summary_homer

**Pipeline provenance:** `snakemake-workflows-chipseq-finish` (family: `chipseq`, stage: `late`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given `input/homer_summary.tsv` (sample × feature wide counts TSV).
Pivot it to long format by gathering `exon, Intergenic, intron, promoter-TSS,
TTS` into columns `sequence_element, counts` (per `tidyr::gather`-style), and
write the resulting tibble to `output/homer_long.tsv` via `readr::write_tsv`.

## Deliverables

- At least `output/homer_long.tsv` must exist when you submit.
- Full output set expected: homer_long.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
