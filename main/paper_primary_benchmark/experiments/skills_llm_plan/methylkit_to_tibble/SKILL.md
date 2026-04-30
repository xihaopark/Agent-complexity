---
name: llm-plan-methylkit-to-tibble
description: >-
  LLM-generated plan skill for task `methylkit_to_tibble` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: methylkit_to_tibble
generated_at: 2026-04-16T17:22:37Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves converting a methylKit object into a long tibble format and then computing the mean methylation per sample and chromosome. The process begins by reading the methylKit object from an RDS file, transforming it into a long format using `pivot_longer` on specific columns related to coverage and methylation counts. Afterward, the data is pivoted to a wide format to calculate the methylation percentage (mCpG) as the ratio of methylated cytosines to coverage. Finally, the mean mCpG is computed for each combination of sample and chromosome, and the results are saved as a TSV file.

## Parameters
- Path to the input RDS file: `input/mk_united.rds`
- Output path for the long tibble: `output/df_mku.rds`
- Output path for the mean mCpG table: `output/mean_mcpg.tsv`
- Columns to pivot: `coverage*`, `numCs*`
- Grouping columns for mean calculation: `sample`, `chr`

## Commands / Code Snippets
```r
library(methylKit)
library(dplyr)
library(tidyr)
library(readr)

# Load the methylKit object
methylBase <- readRDS("input/mk_united.rds")

# Convert to a data frame and pivot longer
df_long <- methylBase %>%
  as.data.frame() %>%
  pivot_longer(cols = starts_with("coverage") | starts_with("numCs"),
               names_to = "metric",
               values_to = "value")

# Save the long format tibble
saveRDS(df_long, "output/df_mku.rds")

# Pivot wider and calculate mCpG
df_wide <- df_long %>%
  pivot_wider(names_from = metric, values_from = value) %>%
  mutate(mCpG = numCs / coverage)

# Calculate mean mCpG per sample and chromosome
mean_mcpg <- df_wide %>%
  group_by(sample, chr) %>%
  summarize(mean_mCpG = mean(mCpG, na.rm = TRUE))

# Write the result to a TSV file
write_tsv(mean_mcpg, "output/mean_mcpg.tsv")
```

## Notes for R-analysis agent
- The `methylKit` package is required to handle the methylBase object.
- Ensure the input RDS file is correctly formatted as a methylKit object.
- The `pivot_longer` and `pivot_wider` functions from `tidyr` are used for data transformation.
- The calculation of mCpG assumes that `numCs` and `coverage` columns are correctly identified and contain non-zero values to avoid division errors.
- Verify that the output TSV file contains the expected columns: `sample`, `chr`, `mean_mCpG`.
