---
name: llm-plan-snakepipes-scrna-merge-coutt
description: >-
  LLM-generated plan skill for task `snakepipes_scrna_merge_coutt` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: snakepipes_scrna_merge_coutt
generated_at: 2026-04-16T19:33:39Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - coutt/plate01_libA.corrected.txt
  - coutt/plate01_libB.corrected.txt
---

## Method
The task involves merging two single-cell RNA sequencing count tables by their `GENEID` using an outer join. The merging process requires prefixing each cell column with the library name and replacing the leading `X` in the column names with an underscore. This will result in a combined table that includes all genes from both libraries, with cell counts appropriately labeled. Additionally, a cell manifest file needs to be created, detailing the sample, plate, library, cell index, and cell name for each cell.

## Parameters
- File paths for input tables: `input/coutt/plate01_libA.corrected.txt`, `input/coutt/plate01_libB.corrected.txt`
- Output file paths: `output/merged_coutt.tsv`, `output/merged_coutt.cell_names.tsv`
- Column name prefix: Library name (`libA`, `libB`)
- Column name transformation: Replace leading `X` with `_`

## Commands / Code Snippets
```r
# Load necessary libraries
library(dplyr)

# Read input files
libA <- read.table("input/coutt/plate01_libA.corrected.txt", header = TRUE, sep = "\t")
libB <- read.table("input/coutt/plate01_libB.corrected.txt", header = TRUE, sep = "\t")

# Rename columns by prefixing with library name and replacing leading 'X'
colnames(libA)[-1] <- paste0("libA_", sub("^X", "_", colnames(libA)[-1]))
colnames(libB)[-1] <- paste0("libB_", sub("^X", "_", colnames(libB)[-1]))

# Merge tables by GENEID using an outer join
merged <- full_join(libA, libB, by = "GENEID")

# Write the merged table to file
write.table(merged, "output/merged_coutt.tsv", sep = "\t", col.names = TRUE, quote = FALSE, row.names = FALSE)

# Create cell manifest
cell_names <- data.frame(
  sample = rep("plate01", ncol(merged) - 1),
  plate = rep("plate01", ncol(merged) - 1),
  library = rep(c("libA", "libB"), each = (ncol(merged) - 1) / 2),
  cell_idx = 1:(ncol(merged) - 1),
  cell_name = colnames(merged)[-1]
)

# Write the cell manifest to file
write.table(cell_names, "output/merged_coutt.cell_names.tsv", sep = "\t", col.names = TRUE, quote = FALSE, row.names = FALSE)
```

## Notes for R-analysis agent
- Use the `dplyr` package for data manipulation, specifically `full_join` for the outer join operation.
- Ensure the input files are read with `header = TRUE` and `sep = "\t"` to correctly parse the tab-separated format.
- The output file `merged_coutt.tsv` should be a tab-separated file with column names and without quotes or row names.
- The `merged_coutt.cell_names.tsv` file should include columns for `sample`, `plate`, `library`, `cell_idx`, and `cell_name`, reflecting the structure of the merged count table.
- Double-check the column name transformation to ensure the leading `X` is replaced with an underscore and prefixed with the library name.
