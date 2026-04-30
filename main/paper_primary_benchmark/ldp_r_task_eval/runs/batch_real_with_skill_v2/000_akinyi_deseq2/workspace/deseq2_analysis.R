library(DESeq2)

# Load the data
data <- read.table("input/featureCounts_output.txt", header=TRUE, row.names=1)

# Remove ERCC rows
data <- data[!grepl("^ERCC-", rownames(data)), ]

# Prepare the count matrix and the condition factor
gene_counts <- data[, 6:ncol(data)]
condition <- factor(c(rep("A", 3), rep("B", 3)))

# Create DESeq2 dataset
dds <- DESeqDataSetFromMatrix(countData = gene_counts, colData = data.frame(condition), design = ~ condition)

# Run DESeq2
dds <- DESeq(dds)
res <- results(dds)

# Filter results
diff_res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Split into up and down regulated
diff_up <- diff_res[diff_res$log2FoldChange >= 2, ]
diff_down <- diff_res[diff_res$log2FoldChange <= -2, ]

# Write results
write.table(diff_up, "output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(diff_down, "output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
