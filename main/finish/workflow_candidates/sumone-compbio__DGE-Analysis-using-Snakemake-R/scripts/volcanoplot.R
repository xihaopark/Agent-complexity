

#!/usr/bin/env Rscript

# Load libraries
suppressPackageStartupMessages({
  library(EnhancedVolcano)
  library(readr)
})

# Arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript volcanoplot.R <results_file.csv> <output_plot.png>")
}

res_file <- args[1]
plot_file <- args[2]

# Load DESeq2 results
res <- read_csv(res_file)

# Check required columns
if (!all(c("log2FoldChange", "padj") %in% colnames(res))) {
  stop("The results file must contain 'log2FoldChange' and 'padj' columns")
}

# Pick gene label column
gene_col <- if ("Geneid" %in% colnames(res)) "Geneid" else colnames(res)[1]

# Volcano plot
png(plot_file, width = 2000, height = 1500, res = 300)
EnhancedVolcano(res,
    lab = res[[gene_col]],
    x = "log2FoldChange",
    y = "padj",
    title = "Volcano Plot",
    pCutoff = 0.05,
    FCcutoff = 1,
    pointSize = 2.0,
    labSize = 4.0
)
dev.off()


