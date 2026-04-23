# Load necessary libraries
library(limma)

# Read the expression data
expression_data <- read.csv('input/expression.csv', row.names = 1)

# Read the metadata
metadata <- read.csv('input/metadata.csv')

# Create a design matrix
metadata$group <- factor(metadata$group, levels = c('normal', 'cancer'))
design <- model.matrix(~0 + metadata$group)
colnames(design) <- levels(metadata$group)

# Fit the linear model
fit <- lmFit(expression_data, design)

# Create contrast matrix
contrast_matrix <- makeContrasts(cancer - normal, levels = design)

# Fit the contrasts
fit2 <- contrasts.fit(fit, contrast_matrix)
fit2 <- eBayes(fit2)

# Get the top 250 differentially expressed genes
deg_results <- topTable(fit2, number = 250, sort.by = 'P')

# Write the results to a CSV file
write.csv(deg_results, 'output/deg_results.csv')

# Plot a volcano plot
volcanoplot(fit2, main="Volcano Plot", highlight=250, names=rownames(expression_data))

# Save the plot
png('output/volcano.png')
volcanoplot(fit2, main="Volcano Plot", highlight=250, names=rownames(expression_data))
dev.off()
