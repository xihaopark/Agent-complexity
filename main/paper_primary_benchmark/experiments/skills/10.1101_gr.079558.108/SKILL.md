---
name: paper-10-1101-gr-079558-108
description: >-
  Vision-adapter skill extracted from 10.1101_gr.079558.108.pdf via openai/gpt-4o
source_pdf: 10.1101_gr.079558.108.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The study employs RNA sequencing (RNA-seq) to assess technical reproducibility and compare gene expression levels with microarray data. The core method involves sequencing RNA samples from liver and kidney tissues using the Illumina platform. A Poisson model is used to identify differentially expressed genes, assuming that the number of reads mapping to a gene follows a Poisson distribution. The study also uses a χ² goodness-of-fit test to evaluate lane effects and employs a likelihood ratio test to compare expression levels between groups. The analysis includes identifying novel splice forms by examining exon-exon junctions.

## Parameters
- **Concentration**: 1.5 pM and 3 pM (cDNA concentrations used in sequencing).
- **False Discovery Rate (FDR)**: 0.1% (used for identifying differentially expressed genes).
- **Read Mapping**: Parameters for alignment using ELAND (not specified in detail).

## Commands / Code Snippets
```r
# Poisson model for differential expression
p(x|m) = Hyper(x; C1, C2, x1 + x2)

# χ² goodness-of-fit test
X_ij = Σ ((x_ijk - μ̂_ij)² / μ̂_ij)

# Likelihood ratio test
λ̂_j^A = x_j^A / n_j^A
```

## Notes for R-analysis agent
- Consider using the `edgeR` or `DESeq2` package for differential expression analysis, which can handle Poisson and negative binomial models.
- Ensure input data is pre-processed to remove low-quality reads and align using a suitable aligner like `Bowtie` or `STAR`.
- Validate the assumptions of the Poisson model, especially for genes with low read counts.
- Check for lane effects using the χ² goodness-of-fit test and adjust for batch effects if necessary.
- For splicing analysis, ensure exon-exon junctions are correctly annotated and consider using `rMATS` or similar tools for alternative splicing detection.
```
