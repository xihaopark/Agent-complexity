---
name: llm-plan-chipseq-plot-annotatepeaks-summary-homer
description: >-
  LLM-generated plan skill for task `chipseq_plot_annotatepeaks_summary_homer` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: chipseq_plot_annotatepeaks_summary_homer
generated_at: 2026-04-16T19:35:02Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - homer_summary.tsv
---

## Method
The task involves transforming a wide-format dataset into a long-format tibble using the `tidyr::gather` function. This method is appropriate for reshaping data where multiple columns need to be combined into key-value pairs. The objective specifies gathering the columns `exon, Intergenic, intron, promoter-TSS, TTS` into two new columns named `sequence_element` and `counts`.

## Parameters
- Input file path: `input/homer_summary.tsv`
- Output file path: `output/homer_long.tsv`
- Columns to gather: `exon, Intergenic, intron, promoter-TSS, TTS`
- New column names: `sequence_element`, `counts`

## Commands / Code Snippets
```r
library(tidyr)
library(readr)

# Read the input file
homer_summary <- read_tsv("input/homer_summary.tsv")

# Pivot the data to long format
homer_long <- homer_summary %>%
  gather(key = "sequence_element", value = "counts", exon, Intergenic, intron, promoter-TSS, TTS)

# Write the output file
write_tsv(homer_long, "output/homer_long.tsv")
```

## Notes for R-analysis agent
- Ensure that the `tidyr` and `readr` packages are installed and loaded, as they are essential for data manipulation and file I/O operations.
- The input file `homer_summary.tsv` should be in a tab-separated format with the first row as headers.
- The output file `homer_long.tsv` should also be tab-separated and include the new columns `sequence_element` and `counts`.
- Double-check that the column names in the `gather` function match exactly those in the input file to avoid errors.
