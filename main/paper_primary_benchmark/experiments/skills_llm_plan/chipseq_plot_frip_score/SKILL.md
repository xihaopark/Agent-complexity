---
name: llm-plan-chipseq-plot-frip-score
description: >-
  LLM-generated plan skill for task `chipseq_plot_frip_score` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: chipseq_plot_frip_score
generated_at: 2026-04-16T19:34:55Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - sampleA_control.frip.txt
  - sampleB_control.frip.txt
  - sampleC_control.frip.txt
  - sampleD_control.frip.txt
---

## Method
The task involves processing multiple FRiP score files from a ChIP-seq analysis. The objective is to concatenate these files into a single tibble using `tidyverse` conventions. Each input file contains a single line with a sample identifier and its corresponding FRiP score. The method involves reading each file without headers, combining them into a single data frame, and then writing the result to a TSV file.

## Parameters
- File paths for input files: `input/sampleA_control.frip.txt`, `input/sampleB_control.frip.txt`, `input/sampleC_control.frip.txt`, `input/sampleD_control.frip.txt`
- Output file path: `output/frip_scores.tsv`
- Column names for the tibble: `sample_control`, `frip`

## Commands / Code Snippets
```r
library(tidyverse)

# Read each FRiP file
sampleA <- read.table("input/sampleA_control.frip.txt", header=FALSE, stringsAsFactors=FALSE)
sampleB <- read.table("input/sampleB_control.frip.txt", header=FALSE, stringsAsFactors=FALSE)
sampleC <- read.table("input/sampleC_control.frip.txt", header=FALSE, stringsAsFactors=FALSE)
sampleD <- read.table("input/sampleD_control.frip.txt", header=FALSE, stringsAsFactors=FALSE)

# Combine into a single tibble
frip_scores <- bind_rows(sampleA, sampleB, sampleC, sampleD)

# Assign column names
colnames(frip_scores) <- c("sample_control", "frip")

# Write to TSV
write_tsv(frip_scores, "output/frip_scores.tsv")
```

## Notes for R-analysis agent
- Use the `tidyverse` package for data manipulation, specifically `dplyr` for binding rows and `readr` for writing TSV files.
- Ensure that the input files are read without headers, as specified.
- Verify that the output file `output/frip_scores.tsv` is correctly formatted with the specified column names.
- Double-check that all input files are correctly concatenated into the final tibble.
