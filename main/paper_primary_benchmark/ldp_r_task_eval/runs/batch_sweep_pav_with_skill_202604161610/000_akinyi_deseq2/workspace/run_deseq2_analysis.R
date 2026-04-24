# Load necessary libraries
library(DESeq2)

# Read the count matrix
data <- read.table('input/featureCounts_output.txt', header=TRUE, sep='\t', stringsAsFactors=FALSE)

# Remove rows where Geneid starts with 'ERCC-'
data <- data[!grepl('^ERCC-', data$Geneid), ]

# Extract count data and set rownames
countData <- data[, 7:12]
rownames(countData) <- data$Geneid

# Define condition factor
condition <- factor(c(rep('condition_A', 3), rep('condition_B', 3)))

# Create DESeq2 dataset
colData <- data.frame(condition=condition)
rownames(colData) <- colnames(countData)
dds <- DESeqDataSetFromMatrix(countData=countData, colData=colData, design=~condition)

# Run DESeq2
dds <- DESeq(dds)
res <- results(dds)

# Filter out rows with NA in log2FoldChange or padj
res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]

# Split results
res_up <- res[res$log2FoldChange >= 2, ]
res_down <- res[res$log2FoldChange <= -2, ]

# Write results to files
write.table(res_up, file='output/deseq2_up.txt', col.names=TRUE, row.names=TRUE, quote=FALSE)
write.table(res_down, file='output/deseq2_down.txt', col.names=TRUE, row.names=TRUE, quote=FALSE)
