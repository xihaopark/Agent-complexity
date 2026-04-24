library(limma)
library(edgeR)

# Read input data
counts <- read.table("input/counts.tsv", header = TRUE, row.names = "gene_id")
coldata <- read.table("input/coldata.tsv", header = TRUE, row.names = "sample")

# Ensure sample order matches
counts <- counts[, match(coldata$sample, colnames(counts))]

# Create DGEList
dge <- DGEList(counts = counts, group = coldata$group)
dge <- calcNormFactors(dge)

# Design matrix
design <- model.matrix(~ group, data = coldata)

# Apply voom with quality weights
v <- voomWithQualityWeights(dge, design, plot = FALSE)

# Fit linear model
fit <- lmFit(v, design)
fit <- eBayes(fit)

# Extract results
res <- topTable(fit, coef = 2, number = Inf, sort.by = "none")

# Add gene_id column
res$gene_id <- rownames(res)

# Reorder columns to match required output
res <- res[, c("gene_id", "logFC", "AveExpr", "t", "P.Value", "adj.P.Val")]

# Write output
dir.create("output", showWarnings = FALSE)
write.csv(res, "output/de_results_weighted.csv", row.names = FALSE)

# Submit success
submit_done(success = TRUE)