---
name: paper-10-1186-s13059-019-1670-y
description: >-
  Vision-adapter skill extracted from 10.1186_s13059-019-1670-y.pdf via openai/gpt-4o
source_pdf: 10.1186_s13059-019-1670-y.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
Alevin is an end-to-end pipeline designed to process droplet-based single-cell RNA sequencing data. It performs several key tasks: cell barcode detection, read mapping, unique molecular identifier (UMI) deduplication, gene count estimation, and cell barcode whitelisting. Alevin introduces a novel UMI deduplication algorithm that constructs a parsimonious UMI graph (PUG) to resolve UMI collisions by considering transcript-level information. This approach accounts for both gene-unique reads and reads that map to multiple genes, addressing biases in existing tools that discard gene-ambiguous reads. The pipeline uses a two-step whitelisting procedure to identify cell barcodes, followed by mapping reads to a target transcriptome and deduplicating UMIs using an expectation-maximization algorithm.

## Parameters
- **--keepDuplicates**: Flag to retain duplicate reads even when multiple sequence-identical transcripts exist in the annotation.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- Alevin is implemented in the `salmon` tool, which can be accessed via the `tximport` package in R for downstream analysis.
- Ensure input FASTQ files are sample-demultiplexed.
- Be aware of the memory and thread usage; Alevin is optimized for multi-threading.
- Double-check the whitelisting step and UMI deduplication settings, as these are crucial for accurate gene abundance estimation.
- Consider the impact of discarding multimapping reads on gene count accuracy, especially for genes with low sequence uniqueness.
```
