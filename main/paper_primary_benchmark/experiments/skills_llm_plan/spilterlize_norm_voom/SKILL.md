---
name: llm-plan-spilterlize-norm-voom
description: >-
  LLM-generated plan skill for task `spilterlize_norm_voom` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: spilterlize_norm_voom
generated_at: 2026-04-16T19:33:54Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves normalizing RNA-seq count data using the `limma::voom` method, which is a common approach for transforming count data to log2-counts per million (log-CPM) with associated precision weights. The process begins with creating a `DGEList` object using the `edgeR` package, followed by calculating normalization factors using the TMM (Trimmed Mean of M-values) method. The `voom` function from the `limma` package is then applied to the normalized data to prepare it for linear modeling, with the option to generate a diagnostic plot.

## Parameters
- File path for input counts: `input/filtered_counts.csv`
- File path for output normalized counts: `output/normalized_counts.csv`
- Normalization method for `calcNormFactors`: `'TMM'`
- Normalization method for `voom`: `'none'`
- Span for `voom`: `0.5`
- Plot option for `voom`: `TRUE`

## Commands / Code Snippets
```r
library(edgeR)
library(limma)
library(data.table)

# Load the data
counts <- fread("input/filtered_counts.csv", row.names = 1)

# Create DGEList object
dge <- DGEList(counts = counts)

# Calculate normalization factors
dge <- calcNormFactors(dge, method = "TMM")

# Apply voom transformation
voom_results <- voom(dge, normalize.method = "none", span = 0.5, plot = TRUE)

# Write the normalized counts to a CSV file
fwrite(voom_results$E, file = "output/normalized_counts.csv", row.names = TRUE)
```

## Notes for R-analysis agent
- Ensure that the `edgeR` and `limma` packages are installed and loaded, as they are essential for the `DGEList`, `calcNormFactors`, and `voom` functions.
- The input file `filtered_counts.csv` should have genes as row names and samples as column names.
- The output file `normalized_counts.csv` should contain the `voom_results$E` matrix, which represents the normalized expression values.
- The `voom` function is set to produce a plot, but it should not be saved to disk as per the task instructions.
- Double-check that the `fwrite` function from the `data.table` package is used to write the output, ensuring row names are included.
