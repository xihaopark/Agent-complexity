# Load necessary library
library(UpSetR)

# Read the input data
data <- read.table("input/peak_intersect.tsv", sep="\t", header=FALSE, stringsAsFactors=FALSE)

# Prepare the data for UpSetR
names(data) <- c("Combination", "Size")

# Create a named vector for UpSetR
combination_vector <- setNames(data$Size, data$Combination)

# Generate the UpSet plot
pdf("output/peak_intersect_upset.pdf")
upset(fromExpression(combination_vector),
      order.by = "freq",
      sets = rev(sort(unique(unlist(strsplit(data$Combination, "&"))))),
      nsets = 70)
dev.off()
