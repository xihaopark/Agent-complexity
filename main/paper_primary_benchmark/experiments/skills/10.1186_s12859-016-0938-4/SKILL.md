---
name: paper-10-1186-s12859-016-0938-4
description: >-
  Vision-adapter skill extracted from 10.1186_s12859-016-0938-4.pdf via openai/gpt-4o
source_pdf: 10.1186_s12859-016-0938-4.pdf
pages_processed: 7
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
Seqinspector is a bioinformatics tool designed for the functional enrichment of user-defined lists of genes, transcripts, and ChIP-seq peaks. It utilizes a coverage-based approach to calculate enrichment statistics by analyzing raw genomic bigwig tracks instead of converting genomic coordinates to gene annotations. The tool employs a two-sample t-test to compare ChIP-seq track coverages derived from user-provided genomic ranges against a background set. The background set consists of 1000 random genomic regions, which can be customized by the user. The statistical significance is assessed using a parametric z-score for single-gene exploration.

## Parameters
- **Genome Assembly**: Selection between Mus musculus (mm9, mm10) and Homo sapiens (hg19).
- **Query Input**: Genomic coordinates in bed format or gene symbols.
- **Background Set**: Default is 1000 random genomic regions; user-defined sets are allowed.
- **Statistical Test**: Two-sample t-test for comparing coverage.
- **Output Options**: Includes stack plots, histograms, and gene lists.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- Consider using packages like `rtracklayer` for handling bigwig files and `GenomicRanges` for genomic range operations.
- Ensure the input genomic coordinates are in the correct format (bed or gene symbols).
- Double-check the compatibility of genome assemblies (mm9, mm10, hg19) with the datasets being analyzed.
- Be aware of the statistical assumptions of the two-sample t-test and ensure the data meets these requirements.
- Verify the background set is appropriately defined if not using the default.
```
