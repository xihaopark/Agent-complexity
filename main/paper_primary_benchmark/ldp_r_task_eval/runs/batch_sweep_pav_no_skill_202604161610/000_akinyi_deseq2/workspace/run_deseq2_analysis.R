# Load necessary libraries
library(DESeq2)

# Read the data
counts <- read.table("input/featureCounts_output.txt", header=TRUE, sep="\t")

# Filter out rows starting with 'ERCC-'
counts <- counts[!grepl("^ERCC-", counts$Geneid), ]

# Prepare the DESeq2 dataset
countData <- as.matrix(counts[, 7:12])
colData <- data.frame(condition=factor(c(rep("A", 3), rep("B", 3))))
rownames(countData) <- counts$Geneid

dds <- DESeqDataSetFromMatrix(countData=countData, colData=colData, design=~condition)

# Run DESeq2
dds <- DESeq(dds)
res <- results(dds)

# Filter results
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Write outputs
write.table(res[res$log2FoldChange >= 2, ], "output/deseq2_up.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(res[res$log2FoldChange <= -2, ], "output/deseq2_down.txt", col.names=TRUE, row.names=TRUE, quote=FALSE)
