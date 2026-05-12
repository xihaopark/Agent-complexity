# Paper-Derived Skill: limma duplicateCorrelation for Paired Design

> Source: Smyth et al. (2005) and limma User's Guide
> Method: Handling within-subject correlation in RNA-seq
> Relevance: Paired samples, repeated measures, batch effects

## Key Finding from Paper

For paired designs (same subject measured at multiple time points or
treatments), observations within the same subject are correlated.
Ignoring this correlation leads to:
- Inflated false positive rates
- Loss of statistical power

The `duplicateCorrelation()` function estimates the correlation structure
then incorporates it into `lmFit()` via the `block` parameter.

## Method from Paper

From limma documentation:

> "The duplicateCorrelation function estimates the correlation between
> observations within a block (e.g., subject). The correlation is then
> used by lmFit to fit a linear model with correlated errors."

## Recommended Implementation

```r
library(limma)
library(edgeR)

# Read data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create DGEList with patient info
dge <- DGEList(counts=counts, group=coldata$condition)
dge <- calcNormFactors(dge)

# Design matrix
design <- model.matrix(~ condition, data=coldata)

# Standard voom
v <- voom(dge, design, plot=FALSE)

# CRITICAL: Estimate correlation within patients/subjects
corfit <- duplicateCorrelation(v, design, block=coldata$patient)

# Use estimated correlation in lmFit
fit <- lmFit(
  v,
  design,
  block=coldata$patient,        # blocking variable (patient ID)
  correlation=corfit$consensus  # consensus correlation
)

fit <- eBayes(fit)
res <- topTable(fit, coef=2, number=Inf, sort.by="none")
```

## Critical Parameters

- **`block`**: Factor identifying correlated groups (e.g., patient IDs)
- **`correlation`**: From `duplicateCorrelation()$consensus`
- **Two-step process**: (1) estimate correlation, (2) fit with correlation

## Alternative: Direct Block Design

For some designs, you can include patient as fixed/random effect:
```r
design <- model.matrix(~ patient + condition, data=coldata)
```
But `duplicateCorrelation` is preferred for many blocks.

## Output Format

Write results with: gene_id, logFC, AveExpr, t, P.Value, adj.P.Val, B
