---
name: llm-plan-nearest-gene
description: >-
  LLM-generated plan skill for task `nearest_gene` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: nearest_gene
generated_at: 2026-04-16T19:34:50Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - gene_symbol.tsv
  - t2g.tsv
---

## Method
The task involves annotating a bedtools-closest output file with gene information. This requires joining data from multiple sources: the bedtools-closest output, a transcript-to-gene mapping file, and a gene symbol file. The method involves reading these files into R, performing data joins to map transcript IDs to gene IDs and then to gene symbols, and finally writing the annotated data to a specified output file. The `dplyr` package in R is well-suited for this task due to its powerful data manipulation functions.

## Parameters
- File path for `peaks_with_nearest.bed`
- File path for `t2g.tsv`
- File path for `gene_symbol.tsv`
- Output file path: `output/annotated.bed`
- Column indices for joining: V22 in `peaks_with_nearest.bed`, first column in `t2g.tsv`, and first column in `gene_symbol.tsv`

## Commands / Code Snippets
```r
library(dplyr)

# Read input files
peaks <- read.table("input/peaks_with_nearest.bed", header = FALSE, sep = "\t")
t2g <- read.table("input/t2g.tsv", header = FALSE, sep = "\t")
gene_symbol <- read.table("input/gene_symbol.tsv", header = FALSE, sep = "\t")

# Join peaks with t2g to get GeneID
annotated <- peaks %>%
  left_join(t2g, by = c("V22" = "V1")) %>%
  rename(GeneID = V2.y)

# Join with gene_symbol to get GeneSymbol
annotated <- annotated %>%
  left_join(gene_symbol, by = c("GeneID" = "V1")) %>%
  rename(GeneSymbol = V2.y)

# Select and rename columns as required
output <- annotated %>%
  select(V1:V18, GeneID, GeneSymbol) %>%
  rename(Chromosome = V1, Start = V2, End = V3, Width = V4, Strand = V5, Score = V6,
         nWindows = V7, logFC.up = V8, logFC.down = V9, PValue = V10, FDR = V11,
         direction = V12, rep.test = V13, rep.logFC = V14, best.logFC = V15,
         best.test = V16, best.start = V17, Name = V18, GeneStrand = V19,
         Distance = V20)

# Write to output file
write.table(output, "output/annotated.bed", sep = "\t", row.names = FALSE, quote = FALSE)
```

## Notes for R-analysis agent
- Use the `dplyr` package for data manipulation tasks such as joining and renaming columns.
- Ensure that the input files are read correctly with the appropriate separator (`\t` for tab-separated values).
- The output file should be a tab-separated file with no row names or quotes, as specified.
- Double-check column indices and names during the join operations to ensure correct mapping.
- The final output should match the specified column order and names exactly as described in the objective.
