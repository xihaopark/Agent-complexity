# Load necessary libraries
library(DESeq2)

# Read the input data
counts <- read.table("input/featureCounts_output.txt", header=TRUE, row.names=1)

# Filter out rows where Geneid starts with 'ERCC-'
counts <- counts[!grepl("^ERCC-", rownames(counts)), ]

# Extract the count data and sample information
countData <- as.matrix(counts[, 6:11])
colData <- data.frame(condition=factor(c(rep("A", 3), rep("B", 3))))

# Create DESeq2 dataset
dds <- DESeqDataSetFromMatrix(countData=countData, colData=colData, design=~condition)

# Run DESeq2
dds <- DESeq(dds)

# Get results
res <- results(dds)

# Filter out rows with NA in log2FoldChange or padj
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Split into upregulated and downregulated
upregulated <- res[res$log2FoldChange >= 2, ]
downregulated <- res[res$log2FoldChange <= -2, ]

# Write results to files
write.table(upregulated, "output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(downregulated, "output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
