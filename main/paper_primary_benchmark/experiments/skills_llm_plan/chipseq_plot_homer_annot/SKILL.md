---
name: llm-plan-chipseq-plot-homer-annot
description: >-
  LLM-generated plan skill for task `chipseq_plot_homer_annot` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: chipseq_plot_homer_annot
generated_at: 2026-04-16T19:33:30Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves processing HOMER annotatePeaks output files to summarize feature counts. The method will involve reading each input file, extracting the `Annotation` column, and aggregating counts based on the first whitespace-separated token in this column. The aggregated data will then be reshaped into a wide format matrix with samples as rows and features as columns. Finally, the resulting matrix will be written to a TSV file.

## Parameters
- File paths for input files: `input/sampleA_annot.txt`, `input/sampleB_annot.txt`, `input/sampleC_annot.txt`
- Output file path: `output/homer_annot_summary.tsv`
- Column name for aggregation: `Annotation`

## Commands / Code Snippets
```r
# Load necessary libraries
library(dplyr)
library(tidyr)

# Define input and output file paths
input_files <- c("input/sampleA_annot.txt", "input/sampleB_annot.txt", "input/sampleC_annot.txt")
output_file <- "output/homer_annot_summary.tsv"

# Function to process each file
process_file <- function(file) {
  data <- read.table(file, header = TRUE, sep = "\t")
  data <- data %>%
    mutate(Feature = sapply(strsplit(as.character(Annotation), " "), `[`, 1)) %>%
    count(Feature) %>%
    spread(Feature, n, fill = 0)
  return(data)
}

# Process each file and combine results
results <- lapply(input_files, process_file)
combined_results <- do.call(rbind, results)

# Write the combined results to a TSV file
write.table(combined_results, file = output_file, sep = "\t", row.names = FALSE, col.names = TRUE, quote = FALSE)
```

## Notes for R-analysis agent
- Use the `dplyr` package for data manipulation and `tidyr` for reshaping the data.
- Ensure that the `Annotation` column is correctly parsed and split by whitespace to extract the feature name.
- The input files are expected to be in a tab-separated format with headers.
- The output should be a wide matrix with samples as rows and features as columns, saved as a TSV file.
- Double-check that the `write.table` function parameters match the requirements: tab-separated, no row names, with column names, and without quotes.
