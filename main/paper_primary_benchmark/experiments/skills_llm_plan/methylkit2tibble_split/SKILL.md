---
name: llm-plan-methylkit2tibble-split
description: >-
  LLM-generated plan skill for task `methylkit2tibble_split` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: methylkit2tibble_split
generated_at: 2026-04-16T19:34:29Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves processing methylation data stored in RDS files, each containing a tibble in a long-format. The method involves concatenating these tibbles into a single unified tibble. After concatenation, the data needs to be pivoted wider based on the `metric` column. The calculation of `mCpG` is performed using the formula `mCpG = numCs / coverage`, with rows where `coverage` is zero being excluded. The final step is to group the data by `sample` and `chr`, compute the mean `mCpG` for each group, and save the results to a TSV file.

## Parameters
- `snakemake@input$rds_list`: List of input RDS file paths.
- `output/df_mku_split.rds`: Path to save the concatenated tibble.
- `output/mean_mcpg_split.tsv`: Path to save the mean mCpG results.
- Columns: `chr`, `start`, `metric`, `value`, `sample`, `numCs`, `coverage`.

## Commands / Code Snippets
```r
library(dplyr)
library(tidyr)
library(readr)

# Load and concatenate RDS files
rds_list <- snakemake@input$rds_list
tibbles <- lapply(rds_list, readRDS)
df_mku_split <- bind_rows(tibbles)

# Save concatenated tibble
saveRDS(df_mku_split, "output/df_mku_split.rds")

# Pivot wider and calculate mCpG
df_wide <- df_mku_split %>%
  pivot_wider(names_from = metric, values_from = value) %>%
  filter(coverage > 0) %>%
  mutate(mCpG = numCs / coverage)

# Group by sample and chr, then calculate mean mCpG
mean_mcpg <- df_wide %>%
  group_by(sample, chr) %>%
  summarise(mean_mCpG = mean(mCpG, na.rm = TRUE))

# Write to TSV
write_tsv(mean_mcpg, "output/mean_mcpg_split.tsv")
```

## Notes for R-analysis agent
- Use `dplyr` for data manipulation tasks such as filtering, mutating, and summarizing.
- Use `tidyr` for pivoting the data wider.
- Ensure that the `coverage` column is checked to avoid division by zero.
- The input RDS files should be in a long-format tibble with specific columns as mentioned.
- The output TSV file should contain the mean mCpG values grouped by `sample` and `chr`.
- Double-check that all file paths and column names match those specified in the task objective.
