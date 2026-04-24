# Paper-Derived Skill: limma voomWithQualityWeights

> Source: Ritchie et al. (2015) Nucleic Acids Research
> Paper: limma powers differential expression analyses
> Method: Array weights for sample quality variation
> Relevance: RNA-seq with variable sample quality

## Key Finding from Paper

For RNA-seq data with variable sample quality, the `voomWithQualityWeights()`
function in limma provides better differential expression results by:

1. Estimating precision weights for each gene (voom)
2. Estimating quality weights for each sample (arrayWeights)
3. Combining both in the linear model fit

## Method from Paper

From Ritchie et al. (2015):

> "Array quality weights estimate relative reliability of each sample...
> Low quality arrays are down-weighted in the analysis."

## Recommended Implementation

```r
library(limma)
library(edgeR)

# Read and prepare data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create DGEList
dge <- DGEList(counts=counts, group=coldata$condition)
dge <- calcNormFactors(dge)

# Design matrix
design <- model.matrix(~ condition, data=coldata)

# CRITICAL: Use voomWithQualityWeights instead of standard voom
v <- voomWithQualityWeights(dge, design, plot=FALSE)

# The function returns precision weights in v$weights AND quality weights
# v$targets$weights contains sample quality weights

# Fit linear model WITH quality weights
# Note: voomWithQualityWeights combines both gene and sample weights
fit <- lmFit(v, design)
fit <- eBayes(fit)

# Extract results
res <- topTable(fit, coef=2, number=Inf, sort.by="none")
```

## Critical Parameters

- **`voomWithQualityWeights`**: Must use instead of `voom`
- **Output columns**: v$targets contains sample quality weights
- **Model fit**: lmFit automatically uses combined weights

## When to Use

Use when:
- Sample quality varies across the experiment
- Some samples have systematically lower counts
- Standard voom gives poor results

## Output Format

Write results with: gene_id, logFC, AveExpr, t, P.Value, adj.P.Val, B
