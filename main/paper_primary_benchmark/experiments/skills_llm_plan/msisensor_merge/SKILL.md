---
name: llm-plan-msisensor-merge
description: >-
  LLM-generated plan skill for task `msisensor_merge` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: msisensor_merge
generated_at: 2026-04-16T19:34:18Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves merging multiple MSIsensor output files into a single summary TSV file. The process requires reading each per-sample MSIsensor output, extracting the sample identifier from the file path, and renaming specific columns. The merged data is then written to a TSV file. This task is primarily a data manipulation and aggregation task, which can be efficiently handled using R's data manipulation packages such as `dplyr` and `readr`.

## Parameters
- File path pattern: `results/msi/<sample>/msi_out.txt`
- Output file path: `output/merged_msi.tsv`
- Column renaming:
  - `Total_Number_of_Sites` to `n_all_sites`
  - `Number_of_Unstable_Sites` to `n_unstable_sites`
  - `%` to `msi_score`

## Commands / Code Snippets
```r
library(dplyr)
library(readr)
library(purrr)

# Define the file path pattern
file_paths <- list.files(path = "results/msi", pattern = "msi_out.txt", recursive = TRUE, full.names = TRUE)

# Function to read and process each file
process_file <- function(file_path) {
  sample_id <- strsplit(file_path, "/")[[1]][3]
  read_tsv(file_path) %>%
    mutate(group = sample_id) %>%
    rename(n_all_sites = Total_Number_of_Sites,
           n_unstable_sites = Number_of_Unstable_Sites,
           msi_score = `%`)
}

# Read, process, and combine all files
merged_data <- map_dfr(file_paths, process_file)

# Write the combined data to a TSV file
write_tsv(merged_data, "output/merged_msi.tsv")
```

## Notes for R-analysis agent
- Use the `dplyr` package for data manipulation tasks such as renaming columns and adding new columns.
- Use `readr::read_tsv` and `readr::write_tsv` for reading and writing TSV files.
- Ensure that the file paths are correctly specified and that the sample identifier is accurately extracted from the path.
- Double-check that the column renaming is correctly applied as specified in the objective.
- Verify that the output file `output/merged_msi.tsv` is correctly generated and contains all expected data.
