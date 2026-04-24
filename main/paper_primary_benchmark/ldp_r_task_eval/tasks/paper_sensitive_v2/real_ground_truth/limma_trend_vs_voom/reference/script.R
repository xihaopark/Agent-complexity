#!/usr/bin/env Rscript
# Reference script: Compare limma-trend vs standard voom
# Source: limma User's Guide (Section on limma-trend)

library(limma)
library(edgeR)

# Read data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id", sep="\t")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample", sep="\t")

# Create DGEList
dge <- DGEList(counts=counts, group=coldata$condition)
dge <- calcNormFactors(dge, method="TMM")

# Design matrix
design <- model.matrix(~ condition, data=coldata)

# Method A: limma-trend (paper method for large datasets)
# From paper: "limma-trend uses the mean-variance trend estimated from log-counts directly"
v_trend <- edgeR::cpm(dge, log=TRUE, prior.count=3)
fit_trend <- lmFit(v_trend, design)
fit_trend <- eBayes(fit_trend, trend=TRUE, robust=TRUE)  # KEY: trend=TRUE

# Extract results (limma-trend)
res_trend <- topTable(fit_trend, coef=2, number=Inf, sort.by="P")
write.csv(res_trend, "output/limma_trend_results.csv", row.names=TRUE)

# Method B: Standard voom
# Paper note: "Standard voom uses precision weights and is slower but exact"
v_voom <- voom(dge, design, plot=FALSE)
fit_voom <- lmFit(v_voom, design)
fit_voom <- eBayes(fit_voom, robust=TRUE)

# Extract results (voom)
res_voom <- topTable(fit_voom, coef=2, number=Inf, sort.by="P")
write.csv(res_voom, "output/voom_results.csv", row.names=TRUE)

# Compare methods
correlation <- cor(res_trend$logFC, res_voom$logFC, use="complete.obs")

# Write comparison
timing_info <- c(
  "Method comparison: limma-trend vs voom",
  paste("Correlation of logFC:", round(correlation, 4)),
  "Note: limma-trend is faster for large datasets (n>50)",
  "Both methods should give similar results (correlation > 0.9)"
)
writeLines(timing_info, "output/method_comparison.txt")

cat("limma-trend vs voom comparison complete.\n")
cat("Correlation:", correlation, "\n")
