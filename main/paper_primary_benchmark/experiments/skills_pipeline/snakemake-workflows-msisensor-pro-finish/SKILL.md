---
name: pipeline-snakemake-workflows-msisensor-pro-finish
source_type: pipeline
workflow_id: snakemake-workflows-msisensor-pro-finish
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/snakemake-workflows__microsatellite-instability-detection-with-msisensor-pro
generated_at: 2026-04-16T19:32:30Z
model: openrouter/openai/gpt-4o
files_used: 17
chars_used: 26838
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method

This pipeline is designed for detecting microsatellite instability (MSI) using the `msisensor-pro` tool. It supports two modes of analysis: matched normal and panel of normals. In the matched normal mode, each tumor sample is paired with a corresponding normal sample from the same patient. In the panel of normals mode, a baseline is created from multiple normal samples, allowing MSI detection in tumor samples without matched normal samples. The workflow includes steps to download the reference genome, scan it with `msisensor-pro`, optionally create a panel of normals, perform MSI calling, and aggregate results across samples.

## Parameters

- `sample_sheet`: Path to the sample sheet TSV file.
- `aliases.tumor`: Alias for tumor samples (default: "tumor").
- `aliases.matched_normal`: Alias for matched normal samples (default: "normal").
- `aliases.panel_of_normals`: Alias for panel of normals samples (commented out by default).
- `ref.species`: Species name for the reference genome (default: "homo_sapiens").
- `ref.release`: Release version of the reference genome (default: 114).
- `ref.build`: Build version of the reference genome (default: "GRCh38").

## Commands / Code Snippets

```r
# R script to merge MSI results
log <- file(snakemake@log[[1]], open="wt")
sink(log)
sink(log, type="message")

rlang::global_entrace()

library(tidyverse)

combined_files_with_header <- read_tsv(
    file = snakemake@input[["msi_results"]],
    id = "group"
  ) |>
  rename(
    n_all_sites = Total_Number_of_Sites,
    n_unstable_sites = Number_of_Unstable_Sites,
    msi_score = `%`
  ) |>
  mutate(
    group = str_match(
        group,
        "results/[^/]+/(?<match>[^/]+)/.+"
    )[,"match"]
  )

write_tsv(
    x = combined_files_with_header,
    file = snakemake@output[["tsv"]]
)
```

## Notes for R-analysis agent

- The pipeline uses `msisensor-pro` for MSI detection, which requires BAM files as input. Ensure that these files are properly indexed.
- The R script provided aggregates MSI results using the `tidyverse` package. It reads TSV files containing MSI results, renames columns for clarity, and writes the combined results to a new TSV file.
- The sample sheet must include columns for `sample`, `alias`, and `group`. The `alias` column should match the aliases defined in the configuration.
- Before running the analysis, ensure that the `config.yaml` is correctly set up to specify either matched normal or panel of normals mode, but not both.
- The reference genome details (species, release, build) must match the data used for alignment and recalibration.
