library(limma)

# Load expression data and metadata
datExpr <- read.csv("input/exprs.csv", row.names=1)
metaData <- read.csv("input/meta.csv", row.names=1)

# Prepare design matrix
group <- factor(metaData$group)
design <- model.matrix(~0 + group)
colnames(design) <- levels(group)

# Fit the linear model
fit <- lmFit(datExpr, design)

# Define contrast
contrast <- makeContrasts(cancer - normal, levels=design)

# Apply contrast and compute statistics
fit2 <- contrasts.fit(fit, contrast)
fit2 <- eBayes(fit2)

# Extract top 250 differentially expressed probes
deg_results <- topTable(fit2, adjust="fdr", number=250)

# Save results
write.csv(deg_results, "output/deg_results.csv")