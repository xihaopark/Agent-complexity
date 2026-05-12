library(edgeR)
library(limma)
library(data.table)

# Load the data
data <- fread('input/filtered_counts.csv', data.table=FALSE)
rownames(data) <- data[,1]
data <- data[,-1]

# Create DGEList object
dge <- DGEList(counts=data)

# Normalize using TMM
dge <- calcNormFactors(dge, method='TMM')

# Apply voom transformation
voom_results <- voom(dge, normalize.method='none', span=0.5, plot=TRUE)

# Extract the E matrix
E_matrix <- voom_results$E

# Write the E matrix to a CSV file
fwrite(as.data.frame(E_matrix), file='output/normalized_counts.csv', row.names=TRUE)