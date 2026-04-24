---
name: paper-10-1093-nar-gkv007
description: >-
  Vision-adapter skill extracted from 10.1093_nar_gkv007.pdf via openai/gpt-4o
source_pdf: 10.1093_nar_gkv007.pdf
pages_processed: 8
generator: paper2skills_ab_test/vision_adapter.py
---

```markdown
## Method
The paper describes the `limma` package, which is a part of Bioconductor, designed for differential expression analysis of RNA-seq and microarray data. The core methodology involves fitting linear models to expression data, allowing for the analysis of complex experimental designs. `limma` uses empirical Bayes methods to borrow information across genes, improving variance estimation and statistical power, particularly in small sample sizes. The package supports both RNA-seq and microarray data, using a common analysis pipeline. It incorporates variance modeling to handle technical and biological variability and uses quantitative weights to account for unequal quality in data.

## Parameters
- **voom**: Converts RNA-seq data to log-counts per million with associated precision weights.
- **normalizeBetweenArrays**: Normalizes expression values between samples.
- **arrayWeights**: Estimates relative array variances for weighted analysis.
- **duplicateCorrelation**: Estimates correlation between replicate arrays or samples.
- **makeContrasts**: Defines contrasts for hypothesis testing in linear models.

## Commands / Code Snippets
```r
# Example functions from limma
library(limma)
design <- model.matrix(~ 0 + factor(c(1,1,2,2)))
fit <- lmFit(expressionData, design)
fit <- eBayes(fit)
topTable(fit)
```

## Notes for R-analysis agent
- Use the `limma` package in R for implementation.
- Ensure input data is properly normalized and pre-processed.
- Check for appropriate experimental design matrix setup.
- Verify assumptions of linear modeling and empirical Bayes are met.
- Consider using `voom` for RNA-seq data to handle mean-variance relationships.
- Be cautious of batch effects and include them in the model if necessary.
```
