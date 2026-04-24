#!/usr/bin/env Rscript
# Reference script: limma_duplicatecorrelation
# Based on: epigen-dea_limma workflow
# Key method: duplicateCorrelation for paired/block design
# Reason: paired samples have correlation that must be accounted for

library(limma)
library(edgeR)

counts_path <- "input/counts.tsv"
coldata_path <- "input/coldata.tsv"
output_path <- "output/paired_de.csv"

# Read
counts_data <- read.table(counts_path, header=TRUE, row.names="gene_id", sep="\t")
col_data <- read.table(coldata_path, header=TRUE, row.names="sample", sep="\t")

samples <- intersect(colnames(counts_data), rownames(col_data))
counts_data <- counts_data[, samples]
col_data <- col_data[samples, , drop=FALSE]

# Factors
col_data$patient <- factor(col_data$patient)
col_data$treatment <- factor(col_data$treatment)

# DGEList + voom
dge <- DGEList(counts_data)
dge <- calcNormFactors(dge)

# Design: ~ treatment (main effect), patient will be handled via correlation
design <- model.matrix(~ treatment, data=col_data)

# Voom
v <- voom(dge, design, plot=FALSE)

# Estimate correlation within patient blocks
# This is the key step for paired design
corfit <- duplicateCorrelation(v, design, block=col_data$patient)
cat(sprintf("Estimated correlation: %.3f\n", corfit$consensus))

# Fit with block structure
fit <- lmFit(v, design, block=col_data$patient, correlation=corfit$consensus)
fit <- eBayes(fit)

# Results
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
cat("limma duplicateCorrelation analysis complete.\n")
cat(sprintf("Consensus correlation: %.3f\n", corfit$consensus))
