# Pipeline Skill: limma-voom Differential Expression

> Extracted from: epigen/dea_limma workflow
> Generated: Auto-extracted generic code patterns

## Code Template

```r
library(limma)
library(edgeR)

# Read data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create DGEList and normalize
dge <- DGEList(counts=counts, group=coldata$condition)
dge <- calcNormFactors(dge, method="TMM")

# Create design matrix
design <- model.matrix(~ condition, data=coldata)

# Standard voom transform
v <- voom(dge, design, plot=FALSE)

# Fit linear model
fit <- lmFit(v, design)

# eBayes moderation
fit <- eBayes(fit)

# Extract results
res <- topTable(fit, coef=2, number=Inf, sort.by="none")

# Write output
write.csv(res, "output/de_results.csv")
```

## Common Parameters

- `calcNormFactors`: Use `method="TMM"` for standard RNA-seq
- `voom`: Standard transform without quality weights
- `design`: Simple two-group comparison with `~ condition`

## Notes

This is the standard limma-voom workflow. For samples with quality issues,
consider using `voomWithQualityWeights()` instead of standard `voom()`.
