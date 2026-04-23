# Load necessary libraries
library(limma)

# Read the expression and metadata files
exprs <- read.csv("input/exprs.csv", row.names=1)
meta <- read.csv("input/meta.csv")

# Prepare the design matrix
meta$group <- factor(meta$group, levels = c("normal", "cancer"))
design <- model.matrix(~0 + meta$group)
colnames(design) <- levels(meta$group)

# Fit the linear model
fit <- lmFit(exprs, design)

# Define the contrast matrix
contrast.matrix <- makeContrasts(cancer - normal, levels=design)

# Fit the contrasts
fit2 <- contrasts.fit(fit, contrast.matrix)

# Apply empirical Bayes smoothing
fit2 <- eBayes(fit2)

# Extract the top 250 differentially expressed probes
results <- topTable(fit2, adjust="fdr", number=250)

# Save the results to a CSV file
write.csv(results, file="output/deg_results.csv")