---
name: llm-plan-riya-limma
description: >-
  LLM-generated plan skill for task `riya_limma` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: riya_limma
generated_at: 2026-04-16T19:33:14Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - meta.csv
---

## Method
The task involves differential expression analysis using the limma package in R. The objective is to identify the top 250 differentially expressed probes between cancer and normal groups from pre-normalised expression data. The analysis will use the `lmFit` function to fit a linear model to the expression data, followed by `makeContrasts` to specify the contrast of interest (cancer vs normal). The `eBayes` function will be applied to compute empirical Bayes statistics, and `topTable` will be used to extract the top 250 probes based on adjusted p-values using the FDR method.

## Parameters
- File path for expression data: `input/exprs.csv`
- File path for metadata: `input/meta.csv`
- Group column in metadata: `group`
- Contrast of interest: `cancer - normal`
- Number of top probes to extract: 250
- Output file path: `output/deg_results.csv`

## Commands / Code Snippets
```r
# Load necessary libraries
library(limma)

# Read in the data
exprs <- read.csv("input/exprs.csv", row.names = 1)
meta <- read.csv("input/meta.csv", row.names = 1)

# Create design matrix
design <- model.matrix(~ 0 + meta$group)
colnames(design) <- levels(meta$group)

# Fit the linear model
fit <- lmFit(exprs, design)

# Define the contrast
contrast.matrix <- makeContrasts(cancer - normal, levels = design)

# Apply the contrast
fit2 <- contrasts.fit(fit, contrast.matrix)

# Compute empirical Bayes statistics
fit2 <- eBayes(fit2)

# Extract the top 250 differentially expressed probes
topTableResults <- topTable(fit2, adjust = "fdr", number = 250)

# Write the results to a CSV file
write.csv(topTableResults, "output/deg_results.csv")
```

## Notes for R-analysis agent
- Ensure the limma package is installed and loaded.
- The input expression data should have probes as rows and samples as columns.
- The metadata file should have a `group` column indicating the sample group (cancer vs normal).
- The design matrix should be constructed correctly to reflect the groups in the metadata.
- Double-check that the contrast is specified correctly as `cancer - normal`.
- The output should be a CSV file named `deg_results.csv` in the `output/` directory.
- Ensure that the number of top probes extracted is exactly 250, as specified.
