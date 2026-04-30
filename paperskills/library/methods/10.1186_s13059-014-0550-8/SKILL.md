---
name: paper-10-1186-s13059-014-0550-8
description: >-
  Vision-adapter skill extracted from 10.1186_s13059-014-0550-8.pdf via openai/gpt-4o
source_pdf: 10.1186_s13059-014-0550-8.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
DESeq2 is a method for differential analysis of count data, particularly RNA-seq data, which uses shrinkage estimation for dispersions and fold changes to improve stability and interpretability. It employs a generalized linear model (GLM) framework with a negative binomial distribution to model count data. The method involves empirical Bayes shrinkage to estimate dispersion and fold changes, which helps in handling the variability between replicates and low count data. The shrinkage is applied to the dispersion estimates and logarithmic fold changes (LFCs), reducing noise and bias, especially for genes with low counts. DESeq2 also uses a Wald test for hypothesis testing of differential expression, and it incorporates automatic independent filtering to control the false discovery rate (FDR).

## Parameters
- **Normalization factors (sij)**: Used to account for differences in sequencing depth and other technical biases.
- **Shrinkage degree (di)**: Controls the amount of shrinkage applied based on sample size and degrees of freedom.
- **Threshold for LFC (θ)**: Used for hypothesis testing to determine significant differential expression.

## Commands / Code Snippets
```r
# Example DESeq2 usage in R
library(DESeq2)
dds <- DESeqDataSetFromMatrix(countData = count_matrix, colData = col_data, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
```

## Notes for R-analysis agent
- Use the `DESeq2` package in R for implementation.
- Ensure input count data is in a matrix format with genes as rows and samples as columns.
- Check for appropriate normalization factors to account for technical biases.
- Be cautious of low count genes as they may require additional filtering or adjustment.
- Verify the assumptions of the negative binomial distribution for the data.
- Consider using the `rlog` transformation for variance stabilization if needed.
```
