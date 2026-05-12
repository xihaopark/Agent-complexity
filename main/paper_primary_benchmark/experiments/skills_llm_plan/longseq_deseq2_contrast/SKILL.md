---
name: llm-plan-longseq-deseq2-contrast
description: >-
  LLM-generated plan skill for task `longseq_deseq2_contrast` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: longseq_deseq2_contrast
generated_at: 2026-04-16T19:32:57Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - samples.tsv
---

## Method
The task involves performing differential expression analysis using the DESeq2 package in R. The objective is to compute contrasts between conditions 'ko' and 'wt' using the DESeq2 object stored in `dds.rds`. The analysis will include applying the `lfcShrink` function with the 'ashr' method to adjust log fold changes. The results will be sorted by adjusted p-values (padj) and written to a TSV file.

## Parameters
- Contrast vector: `c('condition', 'ko', 'wt')`
- Alpha level for significance: `0.05`
- Input DESeq2 object file path: `input/dds.rds`
- Output file path: `output/contrast_results.tsv`

## Commands / Code Snippets
```r
library(DESeq2)

# Load the DESeq2 object
dds <- readRDS("input/dds.rds")

# Perform differential expression analysis
res <- results(dds, contrast=c('condition', 'ko', 'wt'), alpha=0.05)

# Apply log fold change shrinkage
resLFC <- lfcShrink(dds, contrast=c('condition', 'ko', 'wt'), res=res, type='ashr')

# Sort results by adjusted p-value
resLFC <- resLFC[order(resLFC$padj), ]

# Prepare the results data frame
res_df <- data.frame(gene=rownames(resLFC), resLFC)

# Write results to a TSV file
write.table(res_df, file="output/contrast_results.tsv", sep="\t", quote=FALSE, row.names=FALSE)
```

## Notes for R-analysis agent
- Use the DESeq2 package for differential expression analysis and log fold change shrinkage.
- Ensure the DESeq2 object is correctly loaded from `input/dds.rds`.
- The output TSV file should include columns: `gene, baseMean, log2FoldChange, lfcSE, pvalue, padj`.
- Double-check that the contrast vector and alpha level are correctly specified.
- Ensure the results are sorted by the adjusted p-value before writing to the output file.
