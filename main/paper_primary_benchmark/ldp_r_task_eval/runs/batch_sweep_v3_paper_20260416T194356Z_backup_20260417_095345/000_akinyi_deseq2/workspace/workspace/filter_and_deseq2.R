# Load necessary libraries
library(DESeq2)

# Read the data
data <- read.table("input/featureCounts_output.txt", header=TRUE, sep="\t")

# Filter out rows where Geneid starts with 'ERCC-'
data <- data[!grepl("^ERCC-", data$Geneid), ]

# Prepare the count matrix and condition factor
countData <- as.matrix(data[, 7:12])
rownames(countData) <- data$Geneid
condition <- factor(c(rep("A", 3), rep("B", 3)))

# Create DESeqDataSet object
dds <- DESeqDataSetFromMatrix(countData = countData, colData = data.frame(condition), design = ~ condition)

# Run DESeq2
dds <- DESeq(dds)

# Get results and filter out NAs
res <- results(dds)
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Split results into up and down
res_up <- res[res$log2FoldChange >= 2, ]
res_down <- res[res$log2FoldChange <= -2, ]

# Write results to files
write.table(res_up, "output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(res_down, "output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
