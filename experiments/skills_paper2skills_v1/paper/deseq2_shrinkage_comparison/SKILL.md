# Paper-Derived Skill: DESeq2 Shrinkage Estimator Comparison

> Source: Love, Huber & Anders (2014) and Zhu et al. (2018)
> Papers: DESeq2 and apshim/apeglm publications
> Method: Comparing LFC shrinkage estimators
> Relevance: Understanding different shrinkage approaches

## Key Findings from Papers

Three shrinkage estimators available in DESeq2:

1. **`type="normal"`**: Original DESeq2 estimator (normal prior)
   - Good for general use
   - May over-shrink in some cases

2. **`type="ashr"`**: Adaptive shrinkage (Stephens lab)
   - Flexible, uses empirical Bayes
   - Recommended for general use (new default)

3. **`type="apeglm"`**: Adaptive t prior (Zhu et al. 2018)
   - Better for small samples (n < 5)
   - Less bias in effect sizes

## Implementation for Comparison

```r
library(DESeq2)

# Standard workflow
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds)

# Results with coef
res <- results(dds, name="condition_B_vs_A")

# Compare all three shrinkage estimators
res_normal <- lfcShrink(dds, coef=2, type="normal", res=res)
res_ashr <- lfcShrink(dds, coef=2, type="ashr", res=res)
res_apeglm <- lfcShrink(dds, coef=2, type="apeglm", res=res)

# Analysis can compare:
# - Number of significant genes
# - Distribution of LFC estimates
# - Correlation between estimators
```

## Key Recommendations

| Sample Size | Recommended Type |
|------------|-----------------|
| n < 5 per group | `"apeglm"` |
| n ≥ 5 per group | `"ashr"` |
| Legacy analysis | `"normal"` |

## Output Format

For shrinkage comparison, output may include:
- Selected "best" estimator results: gene_id, baseMean, log2FoldChange, lfcSE, stat, pvalue, padj
- Or comparative statistics across all three estimators
