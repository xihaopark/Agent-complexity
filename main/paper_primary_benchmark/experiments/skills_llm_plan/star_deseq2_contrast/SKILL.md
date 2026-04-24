---
name: llm-plan-star-deseq2-contrast
description: >-
  LLM-generated plan skill for task `star_deseq2_contrast` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: star_deseq2_contrast
generated_at: 2026-04-16T17:22:17Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - samples.tsv
---

## Method
The task involves using the DESeq2 package in R to perform differential expression analysis on RNA-seq data. The provided DESeq2 object (`dds.rds`) is used to compute results for the contrast between treated and untreated conditions. The analysis will focus on calculating the log2 fold changes and associated statistics, followed by applying the `lfcShrink` function with the `ashr` method to obtain shrunken log2 fold changes. The results will be sorted by adjusted p-values (padj) and written to a tab-delimited file.

## Parameters
- DESeq2 object file path: `input/dds.rds`
- Contrast: `condition treated vs untreated`
- lfcShrink type: `'ashr'`
- Output file path: `output/contrast_results.tsv`

## Commands / Code Snippets
```r
library(DESeq2)

# Load the DESeq2 object
dds <- readRDS("input/dds.rds")

# Perform the differential expression analysis
res <- results(dds, contrast=c("condition", "treated", "untreated"))

# Apply lfcShrink with ashr method
resLFC <- lfcShrink(dds, contrast=c("condition", "treated", "untreated"), res=res, type="ashr")

# Sort results by adjusted p-value
resLFC <- resLFC[order(resLFC$padj), ]

# Prepare the results data frame
res_df <- data.frame(gene=rownames(resLFC), resLFC)

# Write the results to a tab-delimited file
write.table(res_df, file="output/contrast_results.tsv", sep="\t", row.names=FALSE, quote=FALSE)
```

## Notes for R-analysis agent
- Ensure the DESeq2 package is installed and loaded.
- The input DESeq2 object (`dds.rds`) should be correctly formatted with the design formula `~condition`.
- The contrast is explicitly defined as `condition treated vs untreated`, with `untreated` as the base level.
- The `lfcShrink` function with `type='ashr'` is used to obtain more accurate log2 fold change estimates.
- The output file `contrast_results.tsv` should contain the specified columns and be sorted by the adjusted p-value.
- Double-check that the output file is written without row names and quotes, as specified.
