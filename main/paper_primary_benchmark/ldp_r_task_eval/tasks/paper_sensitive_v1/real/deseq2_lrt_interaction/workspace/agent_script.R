library(DESeq2)

# Read input data
counts <- read.table("input/counts.tsv", header = TRUE, row.names = 1)
coldata <- read.table("input/coldata.tsv", header = TRUE, row.names = 1)

# Create DESeqDataSet with full model (including interaction)
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = coldata,
  design = ~ treatment * time
)

# Pre-filter low-count genes
dds <- dds[rowSums(counts(dds)) >= 10, ]

# Run DESeq2 with LRT, specifying reduced model without interaction
dds <- DESeq(dds, test = "LRT", reduced = ~ treatment + time)

# Extract results
res <- results(dds)

# Convert to data frame and extract relevant columns
res_df <- as.data.frame(res)
res_df$gene_id <- rownames(res_df)

# Reorder columns to match output format
res_df <- res_df[, c("gene_id", "baseMean", "log2FoldChange", "stat", "pvalue", "padj")]

# Drop rows where log2FoldChange is NA (if any)
res_df <- res_df[!is.na(res_df$log2FoldChange), ]

# Write output
write.csv(res_df, "output/interaction_de.csv", row.names = FALSE)

# Submit success
submit_done(success = TRUE)