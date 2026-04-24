# Paper-Derived Skill: limma-trend for Large Datasets

> **Source**: limma User's Guide (Bioconductor)
> **Section**: Differential expression: limma-trend

## Key Finding from Paper

For large RNA-seq datasets (n > 50), limma-trend provides a faster alternative to voom while maintaining accuracy.

## Implementation

### Method A: limma-trend (Fast)

```r
# Convert to log-cpm directly
logCPM <- cpm(dge, log=TRUE, prior.count=3)

# Fit with trend
fit <- lmFit(logCPM, design)
fit <- eBayes(fit, trend=TRUE, robust=TRUE)
```

### Method B: Standard voom

```r
v <- voom(dge, design, plot=FALSE)
fit <- lmFit(v, design)
fit <- eBayes(fit, robust=TRUE)
```

## Key Point

- limma-trend: Uses mean-variance trend on log-counts (faster)
- voom: Uses precision weights (slower but exact)
- Expected correlation: > 0.9

## When to Use

- **limma-trend**: n > 50, speed important
- **voom**: n < 50, exact weights needed
