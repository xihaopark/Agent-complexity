---
name: llm-plan-spilterlize-filter-features
description: >-
  LLM-generated plan skill for task `spilterlize_filter_features` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: spilterlize_filter_features
generated_at: 2026-04-16T19:33:49Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - annotation.csv
---

## Method
The task involves filtering features from a counts matrix using the `edgeR` package's `filterByExpr` function. This method is commonly used in RNA-seq data analysis to remove lowly expressed genes that are unlikely to be informative. The filtering is based on expression levels across groups defined in the annotation file. The `group` parameter is specified using the `group` column from the `annotation.csv` file.

## Parameters
- Path to counts matrix: `input/counts.csv`
- Path to annotation file: `input/annotation.csv`
- Grouping vector: `annot$group`
- Output file path: `output/filtered_counts.csv`

## Commands / Code Snippets
```r
library(edgeR)
library(data.table)

# Load data
counts <- fread("input/counts.csv", data.table=FALSE)
annot <- fread("input/annotation.csv", data.table=FALSE)

# Set row names
rownames(counts) <- counts[, 1]
counts <- counts[, -1]

# Filter by expression
group <- annot$group
keep <- filterByExpr(counts, group=group)
filtered_counts <- counts[keep, ]

# Write output
fwrite(filtered_counts, "output/filtered_counts.csv", row.names=TRUE)
```

## Notes for R-analysis agent
- Ensure that the `edgeR` package is installed and loaded for `filterByExpr`.
- The input counts matrix should have genes as rows and samples as columns, with the first column as gene identifiers.
- The annotation file should have a `group` column to define the experimental groups for filtering.
- The output should be written using `data.table::fwrite` with `row.names=TRUE` to preserve gene identifiers.
- Double-check that the `group` vector is correctly extracted from the annotation file and matches the sample order in the counts matrix.
