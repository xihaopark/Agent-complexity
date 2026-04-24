# Task: limma_trend_vs_voom

**Family**: RNA-seq differential expression  
**Method**: Compare limma-trend vs standard voom for large dataset

## Background

For large RNA-seq datasets (n>50), voom can be computationally expensive. The limma-trend method provides a faster alternative by directly modeling the mean-variance trend on log-counts.

## Objective

Compare limma-trend (fast, approximates voom) vs standard voom (slower, exact) on a dataset with 60 samples.

## Input

- `input/counts.tsv`: 100 genes × 60 samples count matrix
- `input/coldata.tsv`: 60 samples × 2 columns (condition: A/B, batch: 1/2/3)

## Required Steps

1. Read counts and coldata
2. Create DGEList with calcNormFactors
3. **Method A**: limma-trend approach (cpm + trend=TRUE)
4. **Method B**: Standard voom approach
5. Fit both models and extract DE results
6. Compare correlation between methods
7. Output results to `output/`

## Expected Output

- `output/limma_trend_results.csv`: DE results from limma-trend
- `output/voom_results.csv`: DE results from standard voom
- `output/method_comparison.txt`: Correlation and timing comparison

## Paper Reference

From limma User's Guide (Section on limma-trend):
> "The limma-trend method uses the mean-variance trend estimated from log-counts directly, avoiding the need for precision weights. This makes it faster for large datasets while maintaining accuracy."

## Key Point

Agent must recognize that:
- Dataset is large (n=60 > threshold for voom speed concern)
- limma-trend is appropriate alternative
- Both methods should give similar results (correlation > 0.9)
