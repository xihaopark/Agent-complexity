---
name: pipeline-cellranger-multi-finish
source_type: pipeline
workflow_id: cellranger-multi-finish
workflow_dir: main/finish/workflow_candidates/snakemake-workflows__cellranger-multi
generated_at: 2026-04-16T16:56:07Z
model: openrouter/openai/gpt-4o
files_used: 13
chars_used: 47000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method

The pipeline is designed to process single-cell RNA sequencing (scRNA-seq) data using the Cell Ranger software from 10x Genomics. It automates the setup and execution of the `cellranger multi` command, which is used for analyzing multi-modal single-cell data, including gene expression, V(D)J, and feature barcoding assays. The workflow involves several key steps: linking raw FASTQ files to a standardized naming scheme required by Cell Ranger, generating a configuration CSV file for each sample or pool of samples, running the `cellranger multi` command to process the data, and finally, generating summary reports for each sample. The pipeline assumes that users have manually downloaded the Cell Ranger software and reference data, as these are not included due to licensing restrictions.

## Parameters

- `pool_sheet`: Path to the TSV file containing sample information, including pool IDs and feature types.
- `multi_config_csv_sections`: Configuration options for the multi config CSV file, with sub-sections for:
  - `gene-expression`: Options like `reference`, `create-bam`, `expect-cells`, etc.
  - `vdj`: Options like `reference`, `inner-enrichment-primers`.
  - `multiplexing`: Options like `activate` (boolean) and `tsv` (path to multiplexing TSV file).
  - `feature`: Options like `reference`, `r1-length`, `r2-length`.
  - `antigen-specificity`: Options like `control_ids`.

## Commands / Code Snippets

```r
# R script for creating Cell Ranger multi config CSV
log <- file(snakemake@log[[1]], open = "wt")
sink(log)
sink(log, type = "message")

library(rlang)
rlang::global_entrace()

library(tidyverse)
library(cli)

pool_id <- snakemake@wildcards[["pool_id"]]
pool_sheet <- snakemake@input[["pool_sheet"]]

cellranger_fastq_dirs <- enframe(
  snakemake@input[["fq1"]],
  name = NULL,
  value = "filename"
) |>
  separate_wider_regex(
    filename,
    c(
      "results/input/",
      pool_id,
      "_",
      feature_types = "[^/]+",
      "/",
      pool_id,
      "_.+_R1_001.fastq.gz"
    ),
    cols_remove = FALSE
  ) |>
  add_column(
    id = pool_id
  ) |>
  mutate(
    fastqs = normalizePath(dirname(filename)),
    feature_types = str_replace(feature_types, "_", " ")
  ) |>
  select(
    id,
    feature_types,
    fastqs
  ) |>
  distinct()

# Further processing and writing to CSV
```

## Notes for R-analysis agent

- The pipeline uses the `cellranger multi` command from the Cell Ranger suite, which requires a specific directory structure and naming convention for input FASTQ files.
- The R script `create_cellranger_multi_config_csv.R` is used to generate the configuration CSV files needed by Cell Ranger. It relies on the `tidyverse` package for data manipulation.
- Ensure that the reference data paths in the configuration YAML are correctly set to the downloaded reference data directories.
- The pipeline supports multiplexed experiments, which require a separate multiplexing TSV file to map barcodes to samples.
- Check that the `CELLRANGER_TARBALL` environment variable is set to the correct path of the downloaded Cell Ranger tarball before running the pipeline.
- The pipeline assumes that the `pool_sheet` TSV file contains specific columns such as `id`, `feature_types`, `read1`, and `read2`. Ensure these are correctly populated.
