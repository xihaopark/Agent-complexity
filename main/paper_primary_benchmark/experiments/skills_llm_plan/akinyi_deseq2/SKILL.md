---
name: llm-plan-akinyi-deseq2
description: >-
  LLM-generated plan skill for task `akinyi_deseq2` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: akinyi_deseq2
generated_at: 2026-04-16T16:54:11Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves performing differential expression analysis using the DESeq2 package in R. The input is a featureCounts-style count matrix, and the analysis will compare two conditions, A and B, each with three replicates. The method will involve creating a DESeqDataSet object, estimating size factors, dispersions, and fitting a model to test for differential expression between the two conditions. The results will be filtered to identify genes with significant log2 fold changes, specifically those with log2FoldChange >= 2 or <= -2.

## Parameters
- File path to the input count matrix: `input/featureCounts_output.txt`
- Column names for conditions: `sample_0..sample_5`
- Condition labels: `condition_A` for `sample_0..sample_2`, `condition_B` for `sample_3..sample_5`
- Log2 fold change thresholds: `>= 2` for upregulated, `<= -2` for downregulated
- Output file paths: `output/deseq2_up.txt`, `output/deseq2_down.txt`

## Commands / Code Snippets
```r
library(DESeq2)

# Load the data
counts <- read.table("input/featureCounts_output.txt", header=TRUE, row.names=1)
counts <- counts[!grepl("^ERCC-", rownames(counts)), ]

# Prepare the DESeq2 dataset
condition <- factor(c(rep("A", 3), rep("B", 3)))
colData <- data.frame(condition=condition)
dds <- DESeqDataSetFromMatrix(countData=counts[, 7:12], colData=colData, design=~condition)

# Run DESeq2
dds <- DESeq(dds)
res <- results(dds)

# Filter results
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Write upregulated genes
upregulated <- res[res$log2FoldChange >= 2, ]
write.table(upregulated, file="output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)

# Write downregulated genes
downregulated <- res[res$log2FoldChange <= -2, ]
write.table(downregulated, file="output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
```

## Notes for R-analysis agent
- Use the DESeq2 package for differential expression analysis.
- Ensure that the input count matrix is correctly formatted and that ERCC rows are removed before analysis.
- The DESeqDataSet should be constructed using the count data and a colData frame that specifies the conditions.
- Pay attention to filtering out rows with NA values in log2FoldChange or padj before splitting into upregulated and downregulated genes.
- Verify that the output files are written with the correct parameters: `col.names=TRUE`, `row.names=TRUE`, `quote=FALSE`.
