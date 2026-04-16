#!/usr/bin/env Rscript
# ============================
#   Load required libraries
# ============================
suppressMessages({
  library(DESeq2)
  library(tidyverse)
  library(apeglm)
})

# ============================
#   Snakemake inputs/outputs
# ============================
counts_file  <- snakemake@input[["counts"]]
output_file   <- snakemake@output[["csv"]]
contrast_arg  <- snakemake@params[["contrast"]]

output_dir <- dirname(output_file)
if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)

message("Counts file: ", counts_file)
message("Output file: ", output_file)
message("Contrast: ", contrast_arg)

# ============================
#   Load data
# ============================
counts <- read.csv(counts_file, row.names = 1, check.names = FALSE)

# Keep only expression columns (exclude Chr, Start, End, Strand, Length)
expr_counts <- counts[, grep("DUX4|EV|IGH|delta_50", colnames(counts))]

# Metadata
sample_names <- colnames(expr_counts)
conditions <- gsub("_[0-9]+$", "", sample_names)

metadata <- data.frame(
  row.names = sample_names,
  condition = conditions
)
metadata$condition <- factor(metadata$condition)
metadata$condition <- relevel(metadata$condition, ref = "EV")

# ============================
#   Filtering
# ============================
keep <- rowSums(expr_counts) >= 10
counts_filtered <- expr_counts[keep, ]
message("Filtered ", nrow(expr_counts) - nrow(counts_filtered), " low-count genes")

# Save filtered counts with GeneID column
counts_filtered_out <- counts_filtered
counts_filtered_out$gene <- rownames(counts_filtered_out)
counts_filtered_out <- counts_filtered_out[, c("gene", setdiff(names(counts_filtered_out), "gene"))]
write.csv(counts_filtered_out, file.path(output_dir, "filtered_counts.csv"), row.names = FALSE)

# ============================
#   DESeq2
# ============================
dds <- DESeqDataSetFromMatrix(countData = counts_filtered,
                              colData = metadata,
                              design = ~ condition)
dds <- DESeq(dds)

# Normalized counts with GeneID column
norm_counts <- counts(dds, normalized = TRUE)
norm_counts_out <- as.data.frame(norm_counts)
norm_counts_out$gene <- rownames(norm_counts_out)
norm_counts_out <- norm_counts_out[, c("gene", setdiff(names(norm_counts_out), "gene"))]
write.csv(norm_counts_out, file.path(output_dir, "normalized_counts.csv"), row.names = FALSE)

# Parse contrast
contrast_parts <- strsplit(contrast_arg, "_vs_")[[1]]
if (length(contrast_parts) != 2) {
  stop("Contrast argument must be of the form: condition1_vs_condition2")
}
cond1 <- contrast_parts[1]
cond2 <- contrast_parts[2]

res <- results(dds, contrast = c("condition", cond1, cond2))

# Turn rownames into Gene column
res_df <- as.data.frame(res)
res_df$gene <- rownames(res_df)
res_df <- res_df[, c("gene", setdiff(names(res_df), "gene"))]

# Save unshrunk DESeq2 results
write.csv(res_df, file = output_file, row.names = FALSE)

# Shrink LFC
coef_name <- paste0("condition_", cond1, "_vs_", cond2)
if (!(coef_name %in% resultsNames(dds))) {
  stop("Coefficient not found: ", coef_name)
}

resLFC <- lfcShrink(dds, coef = coef_name, type = "apeglm")

# Save shrunk results with gene column
resLFC_df <- as.data.frame(resLFC)
resLFC_df$gene <- rownames(resLFC_df)
resLFC_df <- resLFC_df[, c("gene", setdiff(names(resLFC_df), "gene"))]
write.csv(resLFC_df, file.path(output_dir, "deseq2_results_shrunk.csv"), row.names = FALSE)

# ============================
#   Plots
# ============================
# MA plots
pdf(file.path(output_dir, "MAplot.pdf"))
plotMA(res, ylim = c(-5, 5))
dev.off()

pdf(file.path(output_dir, "MAplot_shrunk.pdf"))
plotMA(resLFC, ylim = c(-5, 5))
dev.off()

# PCA plot
vsd <- vst(dds, blind = FALSE)
pdf(file.path(output_dir, "PCAplot.pdf"))
plotPCA(vsd, intgroup = "condition")
dev.off()

# Dispersion plot
pdf(file.path(output_dir, "dispersion_plot.pdf"))
plotDispEsts(dds)
dev.off()

message("DESeq2 analysis complete. Results and plots saved to ", output_dir)
