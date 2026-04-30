#!/usr/bin/env Rscript
# Reference script for paper-sensitive task: deseq2_apeglm_small_n
# Based on: rna-seq-star-deseq2 workflow (deseq2-init.R + deseq2.R)
# Modification: Use lfcShrink with type="apeglm" instead of "ashr"
# Reason: DESeq2 paper recommends apeglm for low-replicate designs (n=2 vs n=2)

library(DESeq2)

# Input paths (relative to workspace)
counts_path <- "input/counts.tsv"
coldata_path <- "input/coldata.tsv"
output_path <- "output/de_results.csv"

# Read counts
counts_data <- read.table(
  counts_path,
  header = TRUE,
  row.names = "gene_id",
  check.names = FALSE,
  sep = "\t"
)

# Read metadata
col_data <- read.table(
  coldata_path,
  header = TRUE,
  row.names = "sample",
  check.names = FALSE,
  sep = "\t"
)

# Ensure column order matches
samples <- intersect(colnames(counts_data), rownames(col_data))
counts_data <- counts_data[, samples]
col_data <- col_data[samples, , drop = FALSE]

# Set condition as factor with reference level
col_data$condition <- factor(col_data$condition)
col_data$condition <- relevel(col_data$condition, ref = "A")

# Build design: simple ~condition for 2-group comparison
design_formula <- ~ condition

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(
  countData = counts_data,
  colData = col_data,
  design = design_formula
)

# Filter: remove genes with total count <= 1
dds <- dds[rowSums(counts(dds)) > 1, ]

# Run DESeq2 (estimates size factors, dispersions, fits GLM)
dds <- DESeq(dds, parallel = FALSE)

# Get results with coef name (for apeglm we need coef, not contrast)
# Check actual coef names from dds
coef_names <- resultsNames(dds)
coef_name <- coef_names[grep("condition", coef_names)]  # Find condition-related coef

# Results without shrinkage first (for p-values)
res <- results(dds, name = coef_name)

# Shrink log2 fold changes using apeglm (recommended for small n)
# apeglm requires coef=, not contrast=
res_shrunk <- lfcShrink(
  dds,
  coef = coef_name,
  type = "apeglm",
  res = res
)

# Sort by padj (use original res for ordering since apeglm doesn't have padj)
res_shrunk <- res_shrunk[order(res$padj), ]
res <- res[order(res$padj), ]

# Remove NA padj rows
keep <- !is.na(res$padj)
res <- res[keep, ]
res_shrunk <- res_shrunk[keep, ]

# Prepare output data frame
# apeglm results may not have all columns, use what we have
out_df <- data.frame(
  gene_id = rownames(res_shrunk),
  baseMean = res_shrunk$baseMean,
  log2FoldChange = res_shrunk$log2FoldChange,
  lfcSE = res_shrunk$lfcSE,
  pvalue = res$pvalue,  # From original res
  padj = res$padj       # From original res
)

# Write CSV
write.csv(
  out_df,
  file = output_path,
  row.names = FALSE,
  quote = TRUE
)

cat("DESeq2 analysis complete with apeglm shrinkage.\n")
cat(sprintf("Output written to: %s\n", output_path))
cat(sprintf("Genes with padj < 0.05: %d\n", sum(out_df$padj < 0.05, na.rm = TRUE)))
