---
name: llm-plan-star-deseq2-init
description: >-
  LLM-generated plan skill for task `star_deseq2_init` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: star_deseq2_init
generated_at: 2026-04-16T17:22:11Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - samples.tsv
---

## Method
The task involves using the DESeq2 package to analyze RNA-seq count data. The primary method is to create a DESeqDataSet object from the provided count matrix and sample information, with the design formula set to `~condition`. The condition `untreated` is set as the reference level. The DESeq function is then called to perform normalization and differential expression analysis. Rows with a total count of 1 or less are filtered out before analysis.

## Parameters
- File path to `input/counts.tsv`
- File path to `input/samples.tsv`
- Design formula: `~condition`
- Reference level for condition: `untreated`
- Output file path for DESeq2 object: `output/dds.rds`
- Output file path for normalized counts: `output/normalized_counts.tsv`

## Commands / Code Snippets
```r
library(DESeq2)

# Load data
counts <- read.table("input/counts.tsv", header=TRUE, row.names=1)
samples <- read.table("input/samples.tsv", header=TRUE)

# Filter out rows with total count <= 1
counts <- counts[rowSums(counts) > 1, ]

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = samples,
                              design = ~condition)

# Relevel the condition factor
dds$condition <- relevel(dds$condition, ref = "untreated")

# Run DESeq
dds <- DESeq(dds)

# Save DESeq2 object
saveRDS(dds, "output/dds.rds")

# Extract normalized counts
normalized_counts <- counts(dds, normalized=TRUE)

# Write normalized counts to file
write.table(as.data.frame(normalized_counts), file="output/normalized_counts.tsv", sep="\t", row.names=TRUE, col.names=NA)
```

## Notes for R-analysis agent
- Use the DESeq2 package for creating the DESeqDataSet and performing normalization.
- Ensure the input count matrix and sample sheet are correctly formatted and loaded.
- The input count matrix should have genes as rows and samples as columns.
- The `samples.tsv` file should have columns `sample_name` and `condition`.
- Double-check that the `untreated` condition is set as the reference level.
- Ensure that rows with total counts of 1 or less are removed before creating the DESeqDataSet.
- The output normalized counts should be written with gene names as the first column.
