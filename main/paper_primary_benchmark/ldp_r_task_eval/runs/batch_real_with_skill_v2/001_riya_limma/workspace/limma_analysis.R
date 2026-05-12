library(limma)

# Load the data
expression_data <- read.csv('input/expression.csv', row.names = 1)
metadata <- read.csv('input/metadata.csv')

# Create design matrix
design <- model.matrix(~ 0 + factor(metadata$group, levels = c('normal', 'cancer')))
colnames(design) <- levels(factor(metadata$group, levels = c('normal', 'cancer')))

# Fit the linear model
fit <- lmFit(expression_data, design)

# Create contrast matrix
contrast_matrix <- makeContrasts(cancer - normal, levels = design)

# Fit the contrasts
fit2 <- contrasts.fit(fit, contrast_matrix)
fit2 <- eBayes(fit2)

# Get the top differentially expressed genes
deg_results <- topTable(fit2, number = 250)

# Write the results to a CSV file
write.csv(deg_results, 'output/deg_results.csv')

# Create a volcano plot
png('output/volcano.png')
volcanoplot(fit2, main="Volcano plot", highlight=250)
dev.off()
