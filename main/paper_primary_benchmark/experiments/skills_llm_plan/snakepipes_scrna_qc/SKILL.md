---
name: llm-plan-snakepipes-scrna-qc
description: >-
  LLM-generated plan skill for task `snakepipes_scrna_qc` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: snakepipes_scrna_qc
generated_at: 2026-04-16T19:33:45Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  []
---

## Method
The task involves transforming `.libsum` files using the `dcast` function from the `reshape2` package in R. The objective is to pivot the data on the `sample` and `metric` columns, creating two separate output files: one for the `reads` values (`scqc.libstats_reads.tsv`) and another for the `pct` values (`scqc.libstats_pct.tsv`). This transformation will allow for a more structured view of the data, facilitating downstream analysis.

## Parameters
- Input file path: `input/cellsum/`
- Output file paths: `output/scqc.libstats_reads.tsv`, `output/scqc.libstats_pct.tsv`
- Columns for dcast: `sample`, `metric`
- Value variables for dcast: `V3` for reads, `V4` for pct
- Output file settings: `sep='\t'`, `row.names=F`, `quote=F`

## Commands / Code Snippets
```r
library(reshape2)

# List all .libsum files
libsum_files <- list.files(path = "input/cellsum/", pattern = "*.libsum", full.names = TRUE)

# Function to process each .libsum file
process_libsum <- function(file) {
  data <- read.table(file, header = FALSE, sep = "\t")
  colnames(data) <- c("sample", "metric", "V3", "V4")
  
  # Create scqc.libstats_reads.tsv
  reads_data <- dcast(data, sample ~ metric, value.var = "V3")
  write.table(reads_data, file = "output/scqc.libstats_reads.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
  
  # Create scqc.libstats_pct.tsv
  pct_data <- dcast(data, sample ~ metric, value.var = "V4")
  write.table(pct_data, file = "output/scqc.libstats_pct.tsv", sep = "\t", row.names = FALSE, quote = FALSE)
}

# Apply the function to each file
lapply(libsum_files, process_libsum)
```

## Notes for R-analysis agent
- Use the `reshape2` package for the `dcast` function to pivot the data.
- Ensure the input files are read without headers, as specified.
- The output files should be tab-separated with no row names or quotes.
- Verify that the input files are correctly located in the `input/cellsum/` directory and that the output files are written to the `output/` directory.
- Double-check that the correct columns (`V3` for reads and `V4` for pct) are used for the `dcast` operation.
