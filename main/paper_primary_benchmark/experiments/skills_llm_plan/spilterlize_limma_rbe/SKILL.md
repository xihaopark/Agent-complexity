---
name: llm-plan-spilterlize-limma-rbe
description: >-
  LLM-generated plan skill for task `spilterlize_limma_rbe` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: spilterlize_limma_rbe
generated_at: 2026-04-16T19:33:59Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - annotation.csv
---

## Method
The task involves using the `limma` package in R to remove batch effects from gene expression data. The method specified is `limma::removeBatchEffect`, which is designed to adjust for batch effects in high-throughput data. The function will be applied to a matrix of log-scale gene expression data, using batch and group information from an annotation file to construct the design matrix. This approach helps in isolating the biological signal of interest by accounting for unwanted variation due to batch effects.

## Parameters
- Path to `normalized.csv` for gene expression data.
- Path to `annotation.csv` for sample annotations.
- Column `batch` from `annotation.csv` for batch effect removal.
- Column `group` from `annotation.csv` for design matrix construction.
- Output file path: `output/integrated_data.csv`.

## Commands / Code Snippets
```r
# Load necessary libraries
library(limma)
library(data.table)

# Read input files
data <- fread("input/normalized.csv", data.table=FALSE)
annot <- fread("input/annotation.csv", data.table=FALSE)

# Convert data to matrix
data_matrix <- as.matrix(data)

# Create design matrix
design <- model.matrix(~group, data=annot)

# Remove batch effects
corrected_data <- removeBatchEffect(data_matrix, batch=annot$batch, design=design)

# Write output
fwrite(as.data.frame(corrected_data), "output/integrated_data.csv", row.names=TRUE)
```

## Notes for R-analysis agent
- Ensure the `limma` package is installed and loaded for `removeBatchEffect`.
- The input data should be in matrix form for `removeBatchEffect`.
- The `annotation.csv` file must contain `group` and `batch` columns as specified.
- The output should be written using `data.table::fwrite` with `row.names=TRUE` to preserve gene identifiers.
- Double-check that the design matrix is correctly specified using the `group` column from the annotation data.
