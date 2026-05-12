---
name: llm-plan-dea-limma
description: >-
  LLM-generated plan skill for task `dea_limma` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: dea_limma
generated_at: 2026-04-16T19:34:11Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - metadata.tsv
---

## Method
The task involves performing differential expression analysis using the `limma` package in R, which is well-suited for analyzing RNA-seq data. The analysis will follow the limma-voom pipeline, which is designed to handle count data by first normalizing it using TMM (Trimmed Mean of M-values) and then transforming it with the voom function to stabilize the variance. The linear model is fitted using `lmFit`, and empirical Bayes moderation is applied using `eBayes` to improve the statistical power of the analysis. The design matrix will be based on the `treatment` column from the metadata, comparing untreated (`UT`) and treated (`TR`) samples.

## Parameters
- File paths for input data: `input/counts.tsv`, `input/metadata.tsv`
- Output file paths: `output/dea_results.csv`, `output/lmfit.rds`, `output/model_matrix.csv`
- Design formula: `~treatment`
- Treatment groups: `UT`, `TR`

## Commands / Code Snippets
```r
library(limma)
library(edgeR)

# Load data
counts <- read.delim("input/counts.tsv", row.names=1)
metadata <- read.delim("input/metadata.tsv")

# Create DGEList object
dge <- DGEList(counts=counts)
dge <- calcNormFactors(dge, method="TMM")

# Create design matrix
design <- model.matrix(~treatment, data=metadata)

# Apply voom transformation
v <- voom(dge, design)

# Fit linear model
fit <- lmFit(v, design)

# Apply empirical Bayes moderation
fit <- eBayes(fit)

# Write results
results <- topTable(fit, coef="treatmentTR", number=Inf)
write.csv(results, "output/dea_results.csv", row.names=TRUE)

# Save lmFit object
saveRDS(fit, "output/lmfit.rds")

# Write model matrix
write.csv(design, "output/model_matrix.csv", row.names=TRUE)
```

## Notes for R-analysis agent
- Use the `limma` and `edgeR` packages for the analysis, as they provide the necessary functions for TMM normalization, voom transformation, and linear modeling.
- Ensure the input count data is properly formatted with genes as rows and samples as columns.
- The metadata file should have a `treatment` column with values `UT` and `TR` to construct the design matrix.
- The output `dea_results.csv` should include columns for `feature, logFC, AveExpr, t, P.Value, adj.P.Val, B, group`.
- Double-check that the `lmFit` object is saved correctly as an RDS file and that the model matrix is written with row names included.
- Verify that the correct coefficient (`treatmentTR`) is used when extracting results with `topTable`.
