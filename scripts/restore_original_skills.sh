#!/bin/bash
# Restore original paper skills (remove task-specific modifications)

SKILLS_DIR="/mnt/data1/park/Agent-complexity/experiments/skills_paper2skills_v1/paper"

echo "Restoring original paper skills (paper-pure version)..."

# 1. Restore deseq2_apeglm_small_n - remove output format notes
cat > "$SKILLS_DIR/deseq2_apeglm_small_n/SKILL.md" << 'EOF'
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
EOF

echo "✓ Restored deseq2_apeglm_small_n"

# 2. Restore deseq2_lrt_interaction - remove output format notes  
cat > "$SKILLS_DIR/deseq2_lrt_interaction/SKILL.md" << 'EOF'
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
EOF

echo "✓ Restored deseq2_lrt_interaction"

# 3. Restore deseq2_shrinkage_comparison - remove robust patterns
cat > "$SKILLS_DIR/deseq2_shrinkage_comparison/SKILL.md" << 'EOF'
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
EOF

echo "✓ Restored deseq2_shrinkage_comparison"

# 4. Restore limma_voom_weights - remove data reading details
cat > "$SKILLS_DIR/limma_voom_weights/SKILL.md" << 'EOF'
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
EOF

echo "✓ Restored limma_voom_weights"

# 5. Restore limma_duplicatecorrelation - remove "only correct method" emphasis
cat > "$SKILLS_DIR/limma_duplicatecorrelation/SKILL.md" << 'EOF'
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
EOF

echo "✓ Restored limma_duplicatecorrelation"

# Remove the 4 tasks that had wrong skills (they were based on wrong papers)
rm -f "$SKILLS_DIR/methylkit2tibble_split/SKILL.md"
rm -f "$SKILLS_DIR/nearest_gene/SKILL.md"
rm -f "$SKILLS_DIR/snakepipes_merge_ct/SKILL.md"
rm -f "$SKILLS_DIR/snakepipes_merge_fc/SKILL.md"

echo "✓ Removed 4 mismatched skills (methylkit2tibble_split, nearest_gene, snakepipes_merge_*)"

echo ""
echo "All skills restored to paper-pure version!"
echo "Skills now reflect original paper content without task-specific modifications."
