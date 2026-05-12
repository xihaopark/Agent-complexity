---
name: llm-plan-snakepipes-merge-fc
description: >-
  LLM-generated plan skill for task `snakepipes_merge_fc` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: snakepipes_merge_fc
generated_at: 2026-04-16T19:33:02Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves merging multiple per-sample featureCounts output files into a single counts matrix. The most plausible method for this task is to perform an outer join on the `Geneid` column across all input files. This will ensure that all genes present in any of the samples are included in the final matrix. The resulting matrix should have `Geneid` as row names and the sample identifiers (derived from the filenames) as column names.

## Parameters
- File paths for input files: `input/sampleA.counts.txt`, `input/sampleB.counts.txt`, `input/sampleC.counts.txt`, `input/sampleD.counts.txt`
- Output file path: `output/merged_counts.tsv`
- Column to merge on: `Geneid`
- Column names for output: Basenames of input files without `.counts.txt`

## Commands / Code Snippets
```r
# Load necessary library
library(dplyr)

# Define file paths
input_files <- list.files(path = "input", pattern = "*.counts.txt", full.names = TRUE)

# Read and merge files
merged_counts <- Reduce(function(x, y) {
  x <- read.table(x, header = TRUE, sep = "\t")
  y <- read.table(y, header = TRUE, sep = "\t")
  merge(x, y, by = "Geneid", all = TRUE)
}, input_files)

# Set row names and remove unnecessary columns
rownames(merged_counts) <- merged_counts$Geneid
merged_counts <- merged_counts[, -1]

# Write to output file
write.table(merged_counts, file = "output/merged_counts.tsv", sep = "\t", quote = FALSE, col.names = NA)
```

## Notes for R-analysis agent
- Use the `dplyr` package for efficient data manipulation and merging.
- Ensure that the input files are read with `header = TRUE` and `sep = "\t"` to correctly interpret the tab-separated format.
- The merge operation should be an outer join to include all genes from any sample.
- The output file should have `Geneid` as row names and the sample names (without `.counts.txt`) as column headers.
- Double-check that the output file is written with `sep = "\t"`, `quote = FALSE`, and `col.names = NA` to match the required format.
