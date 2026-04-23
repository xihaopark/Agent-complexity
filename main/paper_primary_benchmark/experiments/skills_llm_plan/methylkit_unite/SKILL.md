---
name: llm-plan-methylkit-unite
description: >-
  LLM-generated plan skill for task `methylkit_unite` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: methylkit_unite
generated_at: 2026-04-16T17:22:31Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves using the `methylKit` package in R to process methylation data from multiple samples. The method centers on reading per-sample bismark coverage files using `methylKit::methRead` with specific parameters for minimum coverage and treatment groups. The `methylKit::unite` function is then used to combine these datasets into a single methylBase object, which is subsequently saved. The task also requires generating a summary statistics file in TSV format.

## Parameters
- File paths for input coverage files: `sampleA.bismark.cov`, `sampleB.bismark.cov`, `sampleC.bismark.cov`, `sampleD.bismark.cov`.
- `mincov`: Minimum coverage threshold, set to 4.
- `treatment`: Grouping vector, set to `c(0, 0, 1, 1)`.
- `assembly`: Genome assembly version, set to `mock_v1`.
- `min.per.group`: Minimum number of samples per group, set to 1.
- `destrand`: Logical flag for strand collapsing, set to `FALSE`.
- Output file paths: `output/mk_united.rds`, `output/unite_stats.tsv`.

## Commands / Code Snippets
```r
library(methylKit)

# Read the bismark coverage files
file.list <- list("input/sampleA.bismark.cov", "input/sampleB.bismark.cov",
                  "input/sampleC.bismark.cov", "input/sampleD.bismark.cov")
treatment <- c(0, 0, 1, 1)

# Load data
mk_raw <- methRead(file.list, 
                   pipeline = "bismarkCoverage", 
                   mincov = 4, 
                   treatment = treatment, 
                   assembly = "mock_v1")

# Unite the methylation data
mk_united <- unite(mk_raw, min.per.group = 1, destrand = FALSE)

# Save the united methylBase object
saveRDS(mk_united, file = "output/mk_united.rds")

# Create and save the summary statistics
unite_stats <- data.frame(n_samples = length(mk_raw),
                          n_sites = nrow(mk_united),
                          min_per_group = 1,
                          destrand = FALSE,
                          use_db = FALSE,
                          db_path = NA)
write.table(unite_stats, file = "output/unite_stats.tsv", sep = "\t", row.names = FALSE, col.names = TRUE)
```

## Notes for R-analysis agent
- The `methylKit` package is essential for this task, specifically the `methRead` and `unite` functions.
- Ensure that the input files are correctly formatted as bismark coverage files without headers.
- The output `unite_stats.tsv` should be a single-row TSV file with the specified columns.
- Double-check that the `treatment` vector and `mincov` parameter are correctly applied during the `methRead` step.
- Verify that the `unite` function is called with the correct `min.per.group` and `destrand` parameters.
- Ensure that the RDS and TSV files are saved in the specified output directory.
