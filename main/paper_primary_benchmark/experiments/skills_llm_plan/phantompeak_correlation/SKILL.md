---
name: llm-plan-phantompeak-correlation
description: >-
  LLM-generated plan skill for task `phantompeak_correlation` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: phantompeak_correlation
generated_at: 2026-04-16T19:34:42Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - header.csv
---

## Method
The task involves generating a CSV file that combines a header from a CSV file with data extracted from an RData object. The RData object contains a list with a data frame of shift and cross-correlation values. The method involves reading the header from the CSV file, extracting the relevant data frame from the RData object, and appending the data frame values to the CSV file without including additional headers or row names.

## Parameters
- Path to the header CSV file: `input/header.csv`
- Path to the RData file: `input/run_spp.RData`
- Path to the output CSV file: `output/crosscorr.csv`

## Commands / Code Snippets
```r
# Load the RData file
load("input/run_spp.RData")

# Read the header from the CSV file
header <- readLines("input/header.csv")

# Extract the cross.correlation data frame from the RData object
crosscorr_df <- crosscorr$cross.correlation

# Write the header to the output CSV file
writeLines(header, "output/crosscorr.csv")

# Append the data frame to the CSV file without headers or row names
write.table(crosscorr_df, "output/crosscorr.csv", sep = ",", col.names = FALSE, row.names = FALSE, append = TRUE)
```

## Notes for R-analysis agent
- Ensure the `crosscorr` list and `cross.correlation` data frame exist in the `run_spp.RData` file.
- Use the `load()` function to access the RData object and extract the necessary data frame.
- The `write.table()` function is used to append data to the CSV file without including headers or row names.
- Verify that the output CSV file is correctly formatted with the header followed by the data frame values.
