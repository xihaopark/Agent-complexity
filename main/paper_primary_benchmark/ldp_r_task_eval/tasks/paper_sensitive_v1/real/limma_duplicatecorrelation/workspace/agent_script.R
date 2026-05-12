library(limma)
library(edgeR)

# Read data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create DGEList with treatment info
dge <- DGEList(counts=counts, group=coldata$treatment)
dge <- calcNormFactors(dge)

# Design matrix
design <- model.matrix(~ treatment, data=coldata)

# Standard voom
v <- voom(dge, design, plot=FALSE)

# Estimate correlation within patients/subjects
corfit <- duplicateCorrelation(v, design, block=coldata$patient)

# Use estimated correlation in lmFit
fit <- lmFit(
  v,
  design,
  block=coldata$patient,
  correlation=corfit$consensus
)

fit <- eBayes(fit)

# Extract results
res <- topTable(fit, coef=2, number=Inf, sort.by="none")

# Write output
write.csv(res, "output/paired_de.csv", row.names=FALSE)

submit_done(success=TRUE)