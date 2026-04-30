---
name: llm-plan-chipseq-plot-peaks-count-macs2
description: >-
  LLM-generated plan skill for task `chipseq_plot_peaks_count_macs2` (pre-rollout, objective + inputs only; no paper or pipeline context).
source_type: llm_plan
task_id: chipseq_plot_peaks_count_macs2
generated_at: 2026-04-16T19:34:59Z
model: openrouter/openai/gpt-4o
generator: skills_llm_plan/tools/generate_llm_plan_skill.py
inputs_previewed:
  - sampleA_control.peaks_count.txt
  - sampleB_control.peaks_count.txt
  - sampleC_control.peaks_count.txt
  - sampleD_control.peaks_count.txt
---

## Method
The task involves aggregating peak count data from multiple ChIP-seq samples into a single table. The method requires reading individual peak count files, each containing a sample identifier and a count, and combining them into a unified data frame. This data frame is then saved as a TSV file. The process involves using `read.table` to read each file, `rbind` to concatenate the data frames, and `write.table` to output the final table.

## Parameters
- File paths for input files: `input/sampleA_control.peaks_count.txt`, `input/sampleB_control.peaks_count.txt`, `input/sampleC_control.peaks_count.txt`, `input/sampleD_control.peaks_count.txt`
- Output file path: `output/peaks_count.tsv`

## Commands / Code Snippets
```r
# Read each file into a data frame
sampleA <- read.table("input/sampleA_control.peaks_count.txt", header=FALSE, stringsAsFactors=FALSE)
sampleB <- read.table("input/sampleB_control.peaks_count.txt", header=FALSE, stringsAsFactors=FALSE)
sampleC <- read.table("input/sampleC_control.peaks_count.txt", header=FALSE, stringsAsFactors=FALSE)
sampleD <- read.table("input/sampleD_control.peaks_count.txt", header=FALSE, stringsAsFactors=FALSE)

# Combine all data frames into one
all_samples <- rbind(sampleA, sampleB, sampleC, sampleD)

# Set column names
colnames(all_samples) <- c("sample_control", "count")

# Write the combined data frame to a TSV file
write.table(all_samples, "output/peaks_count.tsv", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)
```

## Notes for R-analysis agent
- Use the `read.table` function with `header=FALSE` and `stringsAsFactors=FALSE` to correctly read the input files.
- Ensure that the `rbind` function is used to concatenate the data frames vertically.
- The output file should be a TSV with columns named `sample_control` and `count`.
- Verify that the output file path is correctly specified as `output/peaks_count.tsv`.
- Double-check that the output file includes column headers and does not include row names or quotes around the data.
