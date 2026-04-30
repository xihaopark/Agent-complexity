library(edgeR)
library(data.table)

# Load the count data
counts <- fread("input/filtered_counts.csv")

# Set row names
rownames(counts) <- counts[[1]]
counts <- counts[,-1]

# Create a DGEList object
dge <- DGEList(counts=counts)

# Apply TMM normalization
dge <- calcNormFactors(dge, method='TMM')

# Calculate log-CPM
log_cpm <- cpm(dge, log=TRUE, prior.count=3)

# Write the output to a CSV file
fwrite(as.data.frame(log_cpm), file="output/all/normTMM.csv", row.names=TRUE)
