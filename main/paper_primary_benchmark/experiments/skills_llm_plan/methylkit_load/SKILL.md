---
name: llm-plan-methylkit-load
description: >-
  LLM-generated plan skill for task `methylkit_load` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: methylkit_load
generated_at: 2026-04-16T17:22:22Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves using the `methylKit` package in R to load methylation data from per-sample bismark coverage files. The `methRead` function from `methylKit` is specifically designed for this purpose, allowing the user to read methylation data into a `methylRawList` object. The function will be configured to read files in the `bismarkCoverage` format, with a minimum coverage threshold of 4. The treatment vector is set to `c(0, 0, 0)`, indicating that all samples are controls, and the assembly is labeled as `mock_v1`. The final object will be saved as an RDS file for further analysis.

## Parameters
- File paths: `input/sampleA.bismark.cov`, `input/sampleB.bismark.cov`, `input/sampleC.bismark.cov`
- Pipeline: `'bismarkCoverage'`
- Minimum coverage: `4`
- Treatment vector: `c(0, 0, 0)`
- Assembly: `'mock_v1'`
- Output file path: `output/mk_raw.rds`

## Commands / Code Snippets
```r
library(methylKit)

# Define file paths
file_paths <- c("input/sampleA.bismark.cov", 
                "input/sampleB.bismark.cov", 
                "input/sampleC.bismark.cov")

# Load methylation data
methyl_data <- methRead(file_paths,
                        pipeline = "bismarkCoverage",
                        mincov = 4,
                        treatment = c(0, 0, 0),
                        assembly = "mock_v1")

# Save the methylRawList object
saveRDS(methyl_data, file = "output/mk_raw.rds")
```

## Notes for R-analysis agent
- The `methylKit` package is required for this task, specifically the `methRead` function.
- Ensure that the input files are in the correct format as expected by `bismarkCoverage`.
- The output should be a single RDS file containing the `methylRawList` object.
- Double-check that the file paths are relative to ensure portability of the serialized object.
- Verify that the minimum coverage threshold is correctly applied and that no plot files are generated.
