library(DESeq2)

# Read input data
counts <- as.matrix(read.table("input/counts.tsv", header = TRUE, row.names = 1))
coldata <- read.table("input/coldata.tsv", header = TRUE, row.names = 1)

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = coldata,
                              design = ~ condition)

# Run DESeq
dds <- DESeq(dds)

# Get the coefficient name for the contrast (assuming condition is a factor with levels A and B)
contrast_name <- paste("condition_", levels(factor(coldata$condition))[2], "_vs_", levels(factor(coldata$condition))[1], sep = "")

# Run lfcShrink with apeglm (primary)
res <- results(dds, contrast = c(1, 0))
res_apeglm <- lfcShrink(dds, contrast = c(1, 0), type = "apeglm", res = res)

# Extract and write final DE table
shrunk_de <- data.frame(
  gene_id = rownames(res_apeglm),
  baseMean = res_apeglm$baseMean,
  log2FoldChange = res_apeglm$log2FoldChange,
  lfcSE = res_apeglm$lfcSE,
  stat = res_apeglm$stat,
  pvalue = res_apeglm$pvalue,
  padj = res_apeglm$padj
)

write.csv(shrunk_de, "output/shrunk_de.csv", row.names = FALSE)

# Submit done with confirmation
submit_done(success = TRUE)