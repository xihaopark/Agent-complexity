---
name: pipeline-fritjoflammers-snakemake-methylanalysis-finish
source_type: pipeline
workflow_id: fritjoflammers-snakemake-methylanalysis-finish
workflow_dir: main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis
generated_at: 2026-04-16T16:55:46Z
model: openrouter/openai/gpt-4o
files_used: 33
chars_used: 80000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
This pipeline is designed for DNA methylation analysis, focusing on differential methylation and related statistical analyses. It utilizes several bioinformatics tools and R packages, including MethylKit for methylation data processing, DSS for differential methylation region (DMR) analysis, and MACAU for association studies. The pipeline processes raw methylation data, performs quality control, normalization, and statistical analysis to identify differentially methylated regions and associations with phenotypic or environmental variables. It assumes the input data is in a format compatible with tools like Bismark or Methyldackel and requires a configuration file to specify parameters and input files.

## Parameters
- `TOOL_LABEL`: The tool used for methylation calling (e.g., "bismark" or "methyldackel").
- `CHROMOSOMES`: List of chromosomes to analyze.
- `OUTPUT_DIR`: Base directory for output files.
- `RUN_NAME`: Name of the current run, used to create output subdirectories.
- `SAMPLESHEET`: Path to the CSV file containing sample information.
- `MACAU.RUNS`: Configuration for MACAU runs, including relatedness matrix and covariates.
- `METHYLKIT.LOW_COV_THRESHOLD`: Minimum coverage threshold for filtering in MethylKit.
- `METHYLKIT.HIGH_COV_THRESHOLD_PERC`: High coverage threshold percentage for filtering in MethylKit.
- `METHYLKIT.EXCLUDE_SAMPLES`: Samples to exclude from MethylKit analysis.
- `RESOURCES`: Resource allocation for different job sizes (e.g., `medium_small_job`, `big_job`).

## Commands / Code Snippets
```r
# Load metadata from CSV and process
load_metadata <- function(fpath, species_metadata, show_col_types = FALSE, subset = NULL) {
  require(readr)
  species_metadata <- species_metadata |> dplyr::mutate(scientific_name = stringi::stri_enc_toutf8(stringr::str_replace(scientific_name, "Oenanthe[[:space:]]", "O. ")))
  df <- readr::read_tsv(fpath, show_col_types = show_col_types, trim_ws = TRUE) |> dplyr::mutate(Species = stringr::str_replace_all(Species, "Oenanthe", "O.")) |> dplyr::mutate(Species = stringr::str_replace_all(Species, "[[:space:]]+", " ")) |> dplyr::mutate(across(everything(), ~ stringr::str_remove(.x, "\\?")))
  return(df)
}

# Calculate PCA on methylation data
calc_PCA <- function(data, metadata = NULL, variance = FALSE, impute = FALSE) {
  require(dplyr)
  require(tidyr)
  require(tibble)
  require(pcaMethods)
  if (is.null(metadata)) {
    metadata <- data |> dplyr::select(c(sample, Species))
  }
  if (any(class(data) %in% c("methylBaseDB", "methylBase"))) {
    mx_mCpG <- methylKit::percMethylation(mku)
    mx_mCpG <- na.omit(mx_mCpG) |> removeConstantColumns()
  }
  pca <- prcomp(mx_mCpG, scale = TRUE)
  if (variance) {
    var_explained <- pca$sdev^2 / sum(pca$sdev^2)
    df_var <- tibble(comp = 1:length(var_explained), var_explained = var_explained)
    return(df_var)
  }
  df_pca <- pca$rotation |> as_tibble(rownames = "sample") |> dplyr::left_join(metadata)
  return(df_pca)
}
```

## Notes for R-analysis agent
- The pipeline uses the `methylKit` package extensively for methylation data processing, including loading, filtering, and uniting methylation data.
- Ensure input files are compatible with the specified `TOOL_LABEL` (e.g., Bismark or Methyldackel).
- The `calc_PCA` function uses `prcomp` for PCA analysis; ensure the input data is correctly pre-processed and contains no constant columns.
- Check that the `MACAU` configuration is correctly set up, including relatedness matrices and covariates, as these are crucial for association analyses.
- Verify that the `METHYLKIT` thresholds for coverage filtering are appropriate for the dataset to avoid losing significant data.
- The pipeline assumes the presence of specific metadata columns; ensure these are correctly formatted and available in the input metadata files.
