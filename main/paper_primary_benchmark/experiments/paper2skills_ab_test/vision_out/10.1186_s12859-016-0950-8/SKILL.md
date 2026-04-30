---
name: paper-10-1186-s12859-016-0950-8
description: >-
  Vision-adapter skill extracted from 10.1186_s12859-016-0950-8.pdf via openai/gpt-4o
source_pdf: 10.1186_s12859-016-0950-8.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
MethPat is a software tool designed to process bisulfite sequencing data following Bismark alignment. It extracts and visualizes epiallelic DNA methylation patterns from multiplex bisulfite amplicon sequencing. The tool summarizes the methylation state of each CpG site and presents the data in a tab-delimited format suitable for further statistical analysis. MethPat also generates HTML files for visualizing DNA methylation patterns, allowing users to arrange patterns by read count or methylation state. This visualization aids in interpreting the diversity and extent of methylation patterns across samples.

## Parameters
- **Input Data**: Bisulfite sequencing data aligned using Bismark.
- **Output Format**: Tab-delimited text and HTML visualization.
- **Visualization Options**: Arrange patterns by read count or methylation state; color customization.

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- MethPat processes output from Bismark; ensure Bismark alignment is completed before using MethPat.
- Check for compatibility with R packages that handle bisulfite sequencing data, such as `methylKit` or `bsseq`.
- Verify input data format matches MethPat requirements (aligned bisulfite sequencing data).
- Consider visualization needs: MethPat provides HTML outputs, which may need conversion for R-based visualization.
```
