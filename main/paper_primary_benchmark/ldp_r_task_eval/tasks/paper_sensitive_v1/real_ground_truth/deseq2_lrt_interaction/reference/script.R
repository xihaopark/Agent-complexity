#!/usr/bin/env Rscript
# Reference script: deseq2_lrt_interaction
# Based on: rna-seq-star-deseq2 workflow
# Key method: Use LRT (likelihood ratio test) for interaction effect
# Full model: ~ treatment * time
# Reduced model: ~ treatment + time
# Reason: Wald test on main effects misses interaction

library(DESeq2)

counts_path <- "input/counts.tsv"
coldata_path <- "input/coldata.tsv"
output_path <- "output/interaction_de.csv"

# Read data
counts_data <- read.table(counts_path, header=TRUE, row.names="gene_id", sep="\t")
col_data <- read.table(coldata_path, header=TRUE, row.names="sample", sep="\t")

# Align samples
samples <- intersect(colnames(counts_data), rownames(col_data))
counts_data <- counts_data[, samples]
col_data <- col_data[samples, , drop=FALSE]

# Factors
col_data$treatment <- factor(col_data$treatment)
col_data$time <- factor(col_data$time)

# Create DESeqDataSet with FULL model (interaction)
# Formula: ~ treatment * time = ~ treatment + time + treatment:time
dds_full <- DESeqDataSetFromMatrix(
  countData = counts_data,
  colData = col_data,
  design = ~ treatment * time
)

dds_full <- dds_full[rowSums(counts(dds_full)) > 1, ]

# DESeq with LRT: full vs reduced (no interaction)
# Reduced model removes the interaction term
dds_full <- DESeq(dds_full, test="LRT", reduced = ~ treatment + time)

# Results for the interaction term
# Check available result names and find interaction coef
coef_names <- resultsNames(dds_full)
interaction_coef <- coef_names[grep("treatment.*time", coef_names)]
if (length(interaction_coef) == 0) {
  interaction_coef <- coef_names[length(coef_names)]  # Last one is usually interaction
}
res <- results(dds_full, name=interaction_coef[1])

# Sort and filter
res <- res[order(res$padj), ]
res <- res[!is.na(res$padj), ]

# Export
out_df <- data.frame(
  gene_id = rownames(res),
  baseMean = res$baseMean,
  log2FoldChange = res$log2FoldChange,
  stat = res$stat,
  pvalue = res$pvalue,
  padj = res$padj
)

write.csv(out_df, output_path, row.names=FALSE, quote=TRUE)
cat("LRT interaction analysis complete.\n")
