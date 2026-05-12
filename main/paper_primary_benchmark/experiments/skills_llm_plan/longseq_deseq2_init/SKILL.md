---
name: llm-plan-longseq-deseq2-init
description: >-
  LLM-generated plan skill for task `longseq_deseq2_init` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: longseq_deseq2_init
generated_at: 2026-04-16T19:32:53Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - samples.tsv
---

## Method
The task involves using the DESeq2 package to perform differential expression analysis on long-read isoform RNA-seq data. The method requires constructing a DESeqDataSet object from a counts matrix, with a design formula based on the `condition` column from the samples metadata. Rows with a total count of 10 or less are filtered out before running the DESeq function to perform the analysis. The results include saving the DESeq2 object and writing normalized counts to a file.

## Parameters
- Path to counts matrix: `input/all_counts.tsv`
- Path to samples metadata: `input/samples.tsv`
- Design formula: `~condition`
- Count threshold for filtering: 10
- Output path for DESeq2 object: `output/dds.rds`
- Output path for normalized counts: `output/normalized_counts.tsv`

## Commands / Code Snippets
```r
library(DESeq2)

# Load data
counts <- read.table("input/all_counts.tsv", header=TRUE, row.names=1)
samples <- read.table("input/samples.tsv", header=TRUE)

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = samples,
                              design = ~condition)

# Filter low count rows
dds <- dds[rowSums(counts(dds)) > 10, ]

# Run DESeq
dds <- DESeq(dds)

# Save DESeq2 object
saveRDS(dds, file="output/dds.rds")

# Write normalized counts
normalized_counts <- counts(dds, normalized=TRUE)
write.table(as.data.frame(normalized_counts), file="output/normalized_counts.tsv", sep="\t", row.names=FALSE)
```

## Notes for R-analysis agent
- Ensure the DESeq2 package is installed and loaded.
- The input counts matrix should have samples as columns and features as rows, with the first column named `Reference`.
- The samples metadata should include `sample` and `condition` columns.
- Verify that the filtering step correctly removes rows with total counts of 10 or less.
- The output file `normalized_counts.tsv` should have `Reference` as the first column, followed by normalized counts for each sample.
- Double-check the paths and filenames to ensure outputs are saved correctly.
