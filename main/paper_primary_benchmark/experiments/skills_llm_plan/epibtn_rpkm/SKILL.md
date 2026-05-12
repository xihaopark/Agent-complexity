---
name: llm-plan-epibtn-rpkm
description: >-
  LLM-generated plan skill for task `epibtn_rpkm` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: epibtn_rpkm
generated_at: 2026-04-16T19:35:07Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - genecount.tsv
  - targets.tsv
---

## Method
The task involves calculating RPKM (Reads Per Kilobase of transcript, per Million mapped reads) values for each gene across different genotypes using featureCounts data. The method requires averaging the counts across replicates for each genotype, joining these averages with gene length information from a BED file, and then computing the RPKM values. The final output is a table with RPKM values for each gene and genotype.

## Parameters
- File paths: `input/genecount.tsv`, `input/targets.tsv`, `input/ref_genes.bed`
- Column names: `GID`, `Sample`, `Replicate`
- Genotype identifiers: `WT`, `KO`
- Output file path: `output/results/RNA/DEG/genes_rpkm__runX__mockref.txt`

## Commands / Code Snippets
```r
# Load necessary libraries
library(dplyr)
library(readr)

# Read input files
genecount <- read_tsv("input/genecount.tsv")
targets <- read_tsv("input/targets.tsv")
ref_genes <- read_tsv("input/ref_genes.bed", col_names = FALSE)

# Filter out rows with GID starting with 'N_'
genecount <- genecount %>% filter(!grepl("^N_", GID))

# Calculate average counts per genotype
avg_counts <- genecount %>%
  gather(key = "Replicate", value = "Count", -GID) %>%
  inner_join(targets, by = "Replicate") %>%
  group_by(GID, Sample) %>%
  summarize(avg = mean(Count))

# Parse gene lengths from ref_genes
ref_genes <- ref_genes %>%
  mutate(GID = sub("ID=gene:", "", V4)) %>%
  mutate(GID = sub(";.*", "", GID)) %>%
  mutate(Length = V3 - V2)

# Join with reference genes and calculate RPKM
all_rpkm <- avg_counts %>%
  inner_join(ref_genes, by = "GID") %>%
  mutate(RPKM = avg * 1000 / Length) %>%
  select(GID, Sample, RPKM)

# Write output
write.table(all_rpkm, "output/results/RNA/DEG/genes_rpkm__runX__mockref.txt", sep = "\t", row.names = FALSE, col.names = TRUE, quote = FALSE)
```

## Notes for R-analysis agent
- Use `dplyr` for data manipulation tasks such as filtering, joining, and summarizing.
- Ensure that the `GID` column in `genecount.tsv` does not contain entries starting with `N_`.
- The `ref_genes.bed` file is headerless; ensure correct column indexing when parsing.
- The `RPKM` calculation requires the gene length, which is derived from the `Start` and `Stop` columns in the BED file.
- Verify that the output file is correctly formatted with tab-separated values and includes headers.
