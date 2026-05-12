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
MethPat is a software tool designed to analyze and visualize complex methylation patterns from bisulfite sequencing data. The tool processes data aligned using Bismark, extracting and summarizing methylation states of CpG sites across multiple epialleles. MethPat provides a visual representation of these patterns, allowing for the identification of methylation heterogeneity within samples. The tool is particularly useful for visualizing the diversity of epiallelic DNA methylation patterns, which are often obscured when data is summarized as average methylation percentages.

## Parameters
- **Input File**: Path to the Bismark-aligned bisulfite sequencing data.
- **Output Format**: Specifies the format for visualizations (e.g., PNG).
- **Visualization Type**: Determines how data is displayed (e.g., by count or percentage).

## Commands / Code Snippets
(No code snippets visible on provided pages.)

## Notes for R-analysis agent
- MethPat is not directly implemented in R but processes Bismark output, which can be integrated into R workflows.
- Ensure Bismark alignment is performed prior to using MethPat.
- Input data should be in a tab-delimited format compatible with MethPat.
- Visualization outputs can be used in R for further analysis or presentation.
- Double-check the bisulfite conversion efficiency, as it impacts the accuracy of methylation state determination.
```
