# Load necessary libraries
library(DESeq2)

# Read the input count matrix
data <- read.table("input/featureCounts_output.txt", header=TRUE, sep="\t")

# Remove rows starting with 'ERCC-'
data <- data[!grepl("^ERCC-", data$Geneid), ]

# Prepare the count data and condition information
countData <- as.matrix(data[, 7:12])
colData <- data.frame(condition=factor(c(rep("A", 3), rep("B", 3))))

# Create DESeqDataSet object
dds <- DESeqDataSetFromMatrix(countData=countData, colData=colData, design=~condition)

# Run DESeq2 differential expression analysis
dds <- DESeq(dds)
res <- results(dds)

# Filter out rows where log2FoldChange or padj is NA
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Split the results into up and down regulated genes
up <- res[res$log2FoldChange >= 2, ]
down <- res[res$log2FoldChange <= -2, ]

# Write the results to output files
write.table(up, "output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(down, "output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
