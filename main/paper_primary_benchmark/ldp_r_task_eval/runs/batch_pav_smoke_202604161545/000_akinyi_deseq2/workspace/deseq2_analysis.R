library(DESeq2)

# Load the data
data <- read.table("input/featureCounts_output.txt", header=TRUE, row.names=1)

# Remove ERCC rows
data <- data[!grepl("^ERCC-", rownames(data)), ]

# Extract count data and condition information
countData <- data[, 6:11]
colData <- data.frame(condition=factor(c(rep("A", 3), rep("B", 3))))

# Create DESeq2 dataset
dds <- DESeqDataSetFromMatrix(countData=countData, colData=colData, design=~condition)

# Run DESeq2
dds <- DESeq(dds)
res <- results(dds)

# Filter results
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Write results for upregulated genes
upregulated <- res[res$log2FoldChange >= 2, ]
write.table(upregulated, file="output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)

# Write results for downregulated genes
downregulated <- res[res$log2FoldChange <= -2, ]
write.table(downregulated, file="output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
