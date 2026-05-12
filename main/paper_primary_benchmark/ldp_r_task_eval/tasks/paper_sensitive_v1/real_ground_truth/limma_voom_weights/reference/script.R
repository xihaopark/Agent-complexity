#!/usr/bin/env Rscript
# Reference script: limma_voom_weights
# Based on: epigen-dea_limma workflow
# Key method: voomWithQualityWeights for unequal sample quality
# Reason: plain voom is sensitive to low-quality samples

library(limma)
library(edgeR)

counts_path <- "input/counts.tsv"
coldata_path <- "input/coldata.tsv"
output_path <- "output/de_results_weighted.csv"

# Read
counts_data <- read.table(counts_path, header=TRUE, row.names="gene_id", sep="\t")
col_data <- read.table(coldata_path, header=TRUE, row.names="sample", sep="\t")

samples <- intersect(colnames(counts_data), rownames(col_data))
counts_data <- counts_data[, samples]
col_data <- col_data[samples, , drop=FALSE]

# DGEList
dge <- DGEList(counts_data)
dge <- calcNormFactors(dge)

# Design
col_data$group <- factor(col_data$group)
design <- model.matrix(~ group, data=col_data)

# Voom with quality weights
# This down-weights low-quality samples automatically
v <- voomWithQualityWeights(dge, design, plot=FALSE)

# Fit with arrayWeights (sample-level weights)
aw <- arrayWeights(v, design)
fit <- lmFit(v, design, weights=aw)
fit <- eBayes(fit)

# Results for group B vs A
res <- topTable(fit, coef=2, number=Inf, sort.by="P")
res <- res[!is.na(res$adj.P.Val), ]

# Export
out_df <- data.frame(
  gene_id = rownames(res),
  logFC = res$logFC,
  AveExpr = res$AveExpr,
  t = res$t,
  P.Value = res$P.Value,
  adj.P.Val = res$adj.P.Val
)

write.csv(out_df, output_path, row.names=FALSE, quote=TRUE)
cat("limma voomWithQualityWeights analysis complete.\n")
