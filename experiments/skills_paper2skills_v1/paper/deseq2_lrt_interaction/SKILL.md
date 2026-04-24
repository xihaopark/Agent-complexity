# Paper-Derived Skill: DESeq2 LRT for Interaction Testing

> Source: DESeq2 vignette and statistical methodology
> Method: Likelihood Ratio Test with nested models
> Relevance: Testing interaction effects between two factors

## Key Finding from Paper

For testing interactions between factors (e.g., genotype × treatment),
the Likelihood Ratio Test (LRT) compares full and reduced models:

- **Full model**: includes interaction term
- **Reduced model**: excludes interaction term
- **Test**: Are genes differentially affected by treatment depending on genotype?

## Method from Paper

```
The LRT examines the ratio of the likelihoods of two models:
- Full:  Y ~ genotype + treatment + genotype:treatment
- Red:   Y ~ genotype + treatment
```

## Recommended Implementation

```r
library(DESeq2)

# Create DESeqDataSet with FULL model (including interaction)
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = coldata,
  design = ~ genotype + treatment + genotype:treatment
)

# Pre-filter
dds <- dds[rowSums(counts(dds)) >= 10, ]

# Run DESeq2 with LRT (not Wald)
# Reduced model removes the interaction term
dds <- DESeq(dds, test="LRT", reduced=~ genotype + treatment)

# Extract results
res <- results(dds)
```

## Critical Parameters

- **`test="LRT"`**: Must specify LRT instead of default Wald
- **`reduced`**: Model formula WITHOUT the interaction term
- **Coefficient interpretation**: LRT tests all coefficients in full but not in reduced

## Alternative: Wald Test for Specific Coefficients

For specific interaction coefficients, you can also use:
```r
res <- results(dds, name="genotypeB.treatmentY")
```

## Output Format

Write results with: gene_id, baseMean, log2FoldChange, stat, pvalue, padj
Note: log2FoldChange not meaningful for LRT (use Wald for LFC)
