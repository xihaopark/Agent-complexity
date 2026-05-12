library(DESeq2)

# Read the featureCounts-style count matrix
data <- read.table("input/featureCounts_output.txt", header=TRUE, stringsAsFactors=FALSE)

# Extract gene names and count data
rownames(data) <- data$Geneid
countdata <- data[, 7:ncol(data)]

# Remove ERCC entries
countdata <- countdata[!grepl("^ERCC-", rownames(countdata)), ]

# Define conditions
conditions <- factor(c(rep("condition_A", 3), rep("condition_B", 3)))
coldata <- data.frame(row.names=colnames(countdata), condition=conditions)

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(countData=countdata, colData=coldata, design=~condition)

# Run DESeq
dds <- DESeq(dds)

# Get results
res <- results(dds)
res <- as.data.frame(res)

# Filter out rows with NA values in log2FoldChange or padj
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Split results into up and down
res_up <- res[res$log2FoldChange >= 2, ]
res_down <- res[res$log2FoldChange <= -2, ]

# Write results to files
write.table(res_up, file="output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(res_down, file="output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
