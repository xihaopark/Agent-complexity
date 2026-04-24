#!/usr/bin/env Rscript
# Reference script: deseq2_shrinkage_comparison
# Based on: rna-seq-star-deseq2 workflow
# Key method: Compare shrinkage estimators
# Primary export: apeglm shrunk results (fast, recommended)
# Also compute ashr for comparison but apeglm is the gold standard here

library(DESeq2)

counts_path <- "input/counts.tsv"
coldata_path <- "input/coldata.tsv"
output_path <- "output/shrunk_de.csv"

# Read
counts_data <- read.table(counts_path, header=TRUE, row.names="gene_id", sep="\t")
col_data <- read.table(coldata_path, header=TRUE, row.names="sample", sep="\t")

samples <- intersect(colnames(counts_data), rownames(col_data))
counts_data <- counts_data[, samples]
col_data <- col_data[samples, , drop=FALSE]

col_data$condition <- factor(col_data$condition)
col_data$condition <- relevel(col_data$condition, ref="A")

# DESeq
dds <- DESeqDataSetFromMatrix(counts_data, col_data, design = ~ condition)
dds <- dds[rowSums(counts(dds)) > 1, ]
dds <- DESeq(dds, parallel=FALSE)

# Results with coef
coef_names <- resultsNames(dds)
coef_name <- coef_names[grep("condition", coef_names)]
res <- results(dds, name=coef_name)

# Use apeglm (recommended for general use)
res_apeglm <- lfcShrink(dds, coef=coef_name, type="apeglm", res=res)

# Sort and filter using original res (apeglm doesn't have padj)
res <- res[order(res$padj), ]
keep <- !is.na(res$padj)
res <- res[keep, ]
res_apeglm <- res_apeglm[keep, ]

# Export apeglm results
# Note: apeglm provides baseMean, log2FoldChange, lfcSE
# pvalue/padj come from original Wald test
out_df <- data.frame(
  gene_id = rownames(res_apeglm),
  baseMean = res_apeglm$baseMean,
  log2FoldChange = res_apeglm$log2FoldChange,
  lfcSE = res_apeglm$lfcSE,
  pvalue = res$pvalue,
  padj = res$padj,
  shrinkage_method = "apeglm"
)

write.csv(out_df, output_path, row.names=FALSE, quote=TRUE)
cat("apeglm shrinkage analysis complete.\n")
