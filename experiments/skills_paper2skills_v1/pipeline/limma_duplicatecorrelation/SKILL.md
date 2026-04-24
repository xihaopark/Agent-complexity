# Pipeline Skill: limma with Paired/Repeated Measures

> Extracted from: epigen/dea_limma workflow (generalized)
> Generated: Adapted for paired design

## Code Template

```r
library(limma)
library(edgeR)

# Read data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create DGEList and normalize
dge <- DGEList(counts=counts, group=coldata$condition)
dge <- calcNormFactors(dge)

# Create design matrix
design <- model.matrix(~ condition, data=coldata)

# Standard voom
v <- voom(dge, design, plot=FALSE)

# Standard lmFit (for independent samples)
fit <- lmFit(v, design)
fit <- eBayes(fit)

# Results
res <- topTable(fit, coef=2, number=Inf)
write.csv(res, "output/de_results.csv")
```

## Common Parameters

- Standard voom workflow for independent samples
- Use `model.matrix` for two-group comparison
- `eBayes` for empirical Bayes moderation

## Notes

This template assumes independent samples. For paired or repeated measures
designs, use `duplicateCorrelation()` with `block` parameter in `lmFit()`.
