# Paper-Derived Skill: DESeq2 apeglm Shrinkage for Small Samples

> Source: Love, Huber & Anders (2014) Genome Biology
> Extracted from: 10.1186/s13059-014-0550-8
> Relevance: Small sample size experiments (n<5 per group)

## Key Finding from Paper

For small sample sizes (typically n < 5 per group), the **apeglm** shrinkage estimator
provides more stable fold change estimates than the default or "ashr" methods.

## Method from Paper

From the DESeq2 paper and apeglm documentation:

> "For small sample sizes, the adaptive t prior of apeglm produces less bias 
> in effect size estimates compared to ashr."

## Recommended Implementation

```r
library(DESeq2)
library(apeglm)

# Standard DESeq2 workflow
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
dds <- DESeq(dds)

# Get unshrunk results first
res <- results(dds, name="condition_B_vs_A")

# Apply apeglm shrinkage (CRITICAL for small samples)
res <- lfcShrink(dds, coef="condition_B_vs_A", type="apeglm", res=res)
```

## Critical Parameters

- **`type="apeglm"`**: Must specify for small samples
- **`coef`**: Use coefficient name from resultsNames(dds)
- **Sample size**: Use when n < 5 per group

## When to Use

Use apeglm shrinkage when:
- Sample size is small (n ≤ 4 per group)
- You need more stable effect size estimates
- LFC estimates show high variance without shrinkage
