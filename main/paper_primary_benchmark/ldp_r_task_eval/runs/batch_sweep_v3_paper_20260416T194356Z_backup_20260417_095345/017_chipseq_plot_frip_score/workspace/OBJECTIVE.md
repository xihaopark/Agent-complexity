# Real R-task: chipseq_plot_frip_score

**Pipeline provenance:** `snakemake-workflows-chipseq-finish` (family: `chipseq`, stage: `late`, difficulty: `1`).
This workspace is derived from a real R script in the source workflow. The ground-truth
reference output used for offline scoring lives outside this workspace and is not
accessible to you during execution.

## Your goal

You are given four per-sample FRiP files under `input/` (`sampleX_control.frip.txt`),
each a single tab-separated line `sample_control\tfrip`.

Concatenate them into a single tibble with columns `sample_control, frip`
using `tidyverse` conventions (read the tables with `read.table(..., header=F,
stringsAsFactors=F)` and `rbind` together). Save the resulting tibble as TSV
at `output/frip_scores.tsv` via `readr::write_tsv`.

## Deliverables

- At least `output/frip_scores.tsv` must exist when you submit.
- Full output set expected: frip_scores.tsv under `output/`.

When the deliverables are in `output/`, call `submit_done(success=true)` with a short
summary of how you solved it.
