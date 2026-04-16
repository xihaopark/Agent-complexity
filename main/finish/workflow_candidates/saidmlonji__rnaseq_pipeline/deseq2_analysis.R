# Install DESeq2 if not already installed
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("DESeq2")

# Load the DESeq2 package
library(DESeq2)

# Simulated count matrix (6 samples, 1000 genes)
set.seed(42)
counts <- matrix(rnbinom(1000 * 6, mu = 10, size = 1), ncol = 6)
rownames(counts) <- paste0("gene", 1:1000)
colnames(counts) <- c("A1", "A2", "A3", "B1", "B2", "B3")

# Sample metadata (3 control, 3 treated)
coldata <- data.frame(
  row.names = colnames(counts),
  condition = factor(c("control", "control", "control", "treated", "treated", "treated"))
)

# Create DESeq2 dataset
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = coldata,
                              design = ~ condition)

# Run DESeq2 pipeline
dds <- DESeq(dds)

# Get differential expression results
res <- results(dds)

# View summary
summary(res)

# View top differentially expressed genes
head(res[order(res$padj), ])

# MA plot
plotMA(res, ylim = c(-5, 5))

# Volcano plot
plot(res$log2FoldChange, -log10(res$pvalue),
     pch = 20,
     col = ifelse(res$padj < 0.05, "red", "black"),
     main = "Volcano Plot",
     xlab = "log2 Fold Change", ylab = "-log10 p-value")
