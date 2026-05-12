# Load necessary libraries
library(limma)

# Read the expression data and metadata
gene_expression <- read.csv('input/expression.csv', row.names=1)
metadata <- read.csv('input/metadata.csv', row.names=1)

# Create design matrix
metadata$group <- factor(metadata$group, levels = c('normal', 'cancer'))
design <- model.matrix(~0 + metadata$group)
colnames(design) <- c('normal', 'cancer')

# Fit the linear model
fit <- lmFit(gene_expression, design)

# Create contrast matrix
contrast.matrix <- makeContrasts(cancer - normal, levels=design)

# Fit the contrasts
fit2 <- contrasts.fit(fit, contrast.matrix)
fit2 <- eBayes(fit2)

# Get top 250 differentially expressed genes
deg_results <- topTable(fit2, number=250, sort.by='P')

# Write results to CSV
write.csv(deg_results, 'output/deg_results.csv')

# Generate a volcano plot
volcanoplot(fit2, highlight=250, names=rownames(gene_expression))
dev.copy(png, 'output/volcano.png')
dev.off()
