---
name: llm-plan-methylkit-filt-norm
description: >-
  LLM-generated plan skill for task `methylkit_filt_norm` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: methylkit_filt_norm
generated_at: 2026-04-16T19:34:24Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves processing methylation data using the `methylKit` package in R. The method includes two main steps: filtering and normalization. First, the `filterByCoverage` function is applied to the `methylRawList` object to filter out CpG sites based on coverage, keeping those with a minimum count of 3 and excluding the top 0.1% of coverage. Next, the `normalizeCoverage` function is used to normalize the coverage across samples using the 'median' method. The processed data is then saved, and summary statistics are generated for each sample.

## Parameters
- `lo.count`: 3 (lower coverage threshold for filtering)
- `hi.perc`: 99.9 (upper coverage percentile for filtering)
- `method`: 'median' (normalization method)
- Input file path: `input/mk_raw.rds`
- Output file paths: `output/mk_filt_norm.rds`, `output/filt_norm_stats.tsv`

## Commands / Code Snippets
```r
library(methylKit)

# Load the methylRawList object
mk_raw <- readRDS("input/mk_raw.rds")

# Filter by coverage
mk_filt <- filterByCoverage(mk_raw, lo.count = 3, hi.perc = 99.9)

# Normalize coverage
mk_norm <- normalizeCoverage(mk_filt, method = "median")

# Save the normalized object
saveRDS(mk_norm, "output/mk_filt_norm.rds")

# Generate per-sample statistics
stats <- getMethylationStats(mk_norm, plot = FALSE)
write.table(stats, "output/filt_norm_stats.tsv", sep = "\t", row.names = FALSE, col.names = TRUE)
```

## Notes for R-analysis agent
- The `methylKit` package is essential for this task, specifically the `filterByCoverage` and `normalizeCoverage` functions.
- Ensure the input file `mk_raw.rds` is a valid `methylRawList` object.
- The output `filt_norm_stats.tsv` should include columns: `sample`, `n_CpGs`, `mean_mCpG`, `mean_coverage`, `median_coverage`.
- Verify that the filtering and normalization steps are correctly applied and that the output files are saved in the specified paths.
- Double-check that the statistics are calculated correctly and match the expected format for the TSV file.
