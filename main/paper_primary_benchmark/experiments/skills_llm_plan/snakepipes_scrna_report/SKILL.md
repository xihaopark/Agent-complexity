---
name: llm-plan-snakepipes-scrna-report
description: >-
  LLM-generated plan skill for task `snakepipes_scrna_report` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: snakepipes_scrna_report
generated_at: 2026-04-16T19:35:14Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - libA.metrics.csv
  - libB.metrics.csv
  - libC.metrics.csv
---

## Method
The task involves merging multiple single-library metric CSV files into a unified TSV report using an outer-merge strategy. Each CSV file contains metrics for a specific library, and some metrics may be missing from individual files. The objective is to read these files, rename the columns to include the library identifier, and perform an outer merge on the 'Metric' column to ensure all metrics are represented in the final report. This approach ensures that any missing metrics in individual libraries are accounted for in the merged output.

## Parameters
- File paths for input CSV files: `input/libA.metrics.csv`, `input/libB.metrics.csv`, `input/libC.metrics.csv`
- Output file path: `output/scrna_report.tsv`
- Column names for merging: `Metric`, `<libID>` (where `<libID>` is the identifier for each library, e.g., `libA`, `libB`, `libC`)

## Commands / Code Snippets
```r
# Read the CSV files
libA <- read.table("input/libA.metrics.csv", header=FALSE, sep=',', as.is=TRUE)
libB <- read.table("input/libB.metrics.csv", header=FALSE, sep=',', as.is=TRUE)
libC <- read.table("input/libC.metrics.csv", header=FALSE, sep=',', as.is=TRUE)

# Rename columns
colnames(libA) <- c("Metric", "libA")
colnames(libB) <- c("Metric", "libB")
colnames(libC) <- c("Metric", "libC")

# Merge the data frames
merged_data <- Reduce(function(x, y) merge(x, y, all=TRUE, by='Metric', sort=FALSE), list(libA, libB, libC))

# Write the merged table to a TSV file
write.table(merged_data, "output/scrna_report.tsv", row.names=FALSE, quote=FALSE, sep='\t')
```

## Notes for R-analysis agent
- Use the `read.table` function with `header=FALSE` and `sep=','` to correctly read the input CSV files without headers.
- Ensure that the column names are correctly renamed to include the library identifiers (`libA`, `libB`, `libC`) for proper merging.
- The `Reduce` function with `merge` and `all=TRUE` ensures an outer join, capturing all metrics across libraries.
- The final output should be written to `output/scrna_report.tsv` using `write.table` with `sep='\t'` to produce a TSV file.
- Double-check that all metrics are included in the final merged output, even if they are missing from some libraries.
