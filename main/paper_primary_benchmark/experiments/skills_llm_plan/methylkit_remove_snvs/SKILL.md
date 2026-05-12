---
name: llm-plan-methylkit-remove-snvs
description: >-
  LLM-generated plan skill for task `methylkit_remove_snvs` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: methylkit_remove_snvs
generated_at: 2026-04-16T19:34:38Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves filtering a methylKit tibble by removing single nucleotide variants (SNVs) specified in a BED file. This is achieved through an anti-join operation, where the tibble is compared against the BED file, and entries matching the SNV positions are excluded. The BED file's `start` position is adjusted from 0-based to 1-based indexing by adding 1. After filtering, the task requires generating a summary of the number of sites before and after exclusion, which is saved as a TSV file.

## Parameters
- Path to `df_united.rds`: `input/df_united.rds`
- Path to `exclusion.bed`: `input/exclusion.bed`
- Output path for filtered tibble: `output/df_united_excl.rds`
- Output path for summary TSV: `output/snv_stats.tsv`

## Commands / Code Snippets
```r
library(dplyr)
library(readr)
library(methylKit)

# Load the methylKit tibble
df_united <- readRDS("input/df_united.rds")

# Load the exclusion BED file
exclusion_bed <- read_tsv("input/exclusion.bed", col_names = c("seqnames", "start", "end", "ref", "alt", "score"))

# Adjust start position to 1-based
exclusion_bed <- exclusion_bed %>% mutate(start = start + 1)

# Perform anti-join to exclude SNVs
df_united_excl <- df_united %>%
  anti_join(exclusion_bed, by = c("seqnames", "start"))

# Save the filtered tibble
saveRDS(df_united_excl, "output/df_united_excl.rds")

# Create summary statistics
n_sites_united <- nrow(df_united)
n_sites_united_excl <- nrow(df_united_excl)

snv_stats <- tibble(
  dataset = c("united", "united_excl"),
  n_sites = c(n_sites_united, n_sites_united_excl)
)

# Write the summary TSV
write_tsv(snv_stats, "output/snv_stats.tsv")
```

## Notes for R-analysis agent
- Use the `dplyr` package for data manipulation, specifically `anti_join` for filtering.
- Ensure the BED file's `start` position is converted from 0-based to 1-based indexing.
- The input tibble should be in a long-format compatible with methylKit.
- Verify that the output files are saved in the specified paths and formats.
- Double-check that the summary TSV includes the correct number of sites before and after exclusion.
