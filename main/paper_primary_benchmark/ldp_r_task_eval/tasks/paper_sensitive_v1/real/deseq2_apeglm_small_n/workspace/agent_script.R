library(DESeq2)
library(apeglm)

# Read input data
counts <- read.table("input/counts.tsv", header = TRUE, row.names = "gene_id", sep = "\t")
coldata <- read.table("input/coldata.tsv", header = TRUE, row.names = "sample", sep = "\t")

# Create DESeq2 dataset
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ condition)

# Run DESeq2
dds <- DESeq(dds)

# Get coefficient name for condition
coef_name <- resultsNames(dds)[2]

# Get unshrunk results
res <- results(dds, contrast = c("condition", "B", "A"))

# Apply apeglm shrinkage
res <- lfcShrink(dds, type = "apeglm", res = res, contrast = c("condition", "B", "A"))

# Extract relevant columns and drop rows with NA padj
de_table <- as.data.frame(res)
de_table <- de_table[!is.na(de_table$padj), c("baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj")]
rownames(de_table) <- rownames(de_table)
de_table$gene_id <- rownames(de_table)

# Reorder columns
de_table <- de_table[, c("gene_id", "baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj")]

# Write output
write.csv(de_table, "output/de_results.csv", row.names = FALSE, quote = TRUE)

# Submit done
submit_done(success = TRUE, message = "Used DESeq2 with apeglm shrinkage for condition B vs A (n=2 vs n=2).")