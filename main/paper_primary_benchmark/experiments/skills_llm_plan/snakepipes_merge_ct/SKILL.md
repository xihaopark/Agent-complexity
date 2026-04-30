---
name: llm-plan-snakepipes-merge-ct
description: >-
  LLM-generated plan skill for task `snakepipes_merge_ct` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: snakepipes_merge_ct
generated_at: 2026-04-16T19:33:07Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves merging multiple Salmon quantification outputs into a single TSV file. The method requires reading each quant.sf file, extracting the TPM column, and merging these columns based on the `Name` column. The sample names for the columns in the merged file are derived from the first token of the file names. This is a straightforward data manipulation task that can be efficiently handled using base R functions or the `dplyr` package for data manipulation.

## Parameters
- File paths for input quant.sf files: `input/WT_A.quant.sf`, `input/WT_B.quant.sf`, `input/KO_A.quant.sf`, `input/KO_B.quant.sf`
- Output file path: `output/merged_tpm.tsv`
- Column to merge on: `Name`
- Column to extract: `TPM`
- Sample name extraction: First token of the file basename

## Commands / Code Snippets
```r
# Load necessary library
library(dplyr)

# Define file paths
files <- list.files(path = "input", pattern = "*.quant.sf", full.names = TRUE)

# Function to read and extract TPM column
read_tpm <- function(file) {
  sample_name <- strsplit(basename(file), "\\.")[[1]][1]
  data <- read.table(file, header = TRUE, sep = "\t")
  data <- data %>% select(Name, TPM) %>% rename(!!sample_name := TPM)
  return(data)
}

# Read and merge all files
merged_data <- Reduce(function(x, y) merge(x, y, by = "Name"), lapply(files, read_tpm))

# Write the merged data to a file
write.table(merged_data, file = "output/merged_tpm.tsv", sep = "\t", quote = FALSE, col.names = NA)
```

## Notes for R-analysis agent
- The `dplyr` package is useful for selecting and renaming columns.
- Ensure that the input files are read correctly with the appropriate separator (`\t`).
- The `merge` function is used to combine data frames by the `Name` column.
- The output file should have `Name` as row names and should not include quotes around the data.
- Double-check that the sample names are correctly extracted from the file names and used as column names in the merged output.
