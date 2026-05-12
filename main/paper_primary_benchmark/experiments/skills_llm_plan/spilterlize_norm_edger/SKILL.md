---
name: llm-plan-spilterlize-norm-edger
description: >-
  LLM-generated plan skill for task `spilterlize_norm_edger` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: spilterlize_norm_edger
generated_at: 2026-04-16T19:34:04Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves normalizing RNA-seq count data using the edgeR package in R. The process includes creating a DGEList object from the count data, applying TMM (Trimmed Mean of M-values) normalization to adjust for library size differences, and then transforming the normalized counts to log-CPM (Counts Per Million) values. This method is suitable for RNA-seq data analysis as it accounts for differences in sequencing depth and provides a log-transformed expression measure that is more suitable for downstream analysis.

## Parameters
- File path for input counts: `input/filtered_counts.csv`
- Method for normalization: `'TMM'`
- Log transformation: `TRUE`
- Prior count for log transformation: `3`
- Output file path: `output/all/normTMM.csv`

## Commands / Code Snippets
```r
library(edgeR)
library(data.table)

# Load the count data
counts <- fread("input/filtered_counts.csv", row.names=1)

# Create a DGEList object
dge <- DGEList(counts=counts)

# Apply TMM normalization
dge <- calcNormFactors(dge, method='TMM')

# Calculate log-CPM
log_cpm <- cpm(dge, log=TRUE, prior.count=3)

# Write the output to a CSV file
fwrite(as.data.frame(log_cpm), file="output/all/normTMM.csv", row.names=TRUE)
```

## Notes for R-analysis agent
- Ensure the edgeR package is installed and loaded for DGEList, calcNormFactors, and cpm functions.
- The input file `filtered_counts.csv` should be formatted with genes as rows and samples as columns.
- The output file `normTMM.csv` should be saved in the specified directory with row names included.
- Double-check that the log transformation and prior count parameters are correctly applied in the cpm function.
- Verify that the output directory exists or is created before writing the output file.
