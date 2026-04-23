# Load necessary library
library(UpSetR)

# Read the input data
data <- read.table('input/peak_intersect.tsv', sep='\t', header=FALSE, stringsAsFactors=FALSE)

# Prepare the data for UpSetR
names(data) <- c('Samples', 'Size')
expression_data <- setNames(data$Size, data$Samples)

# Generate the UpSet plot
pdf('output/peak_intersect_upset.pdf')
upset(fromExpression(expression_data),
      order.by = 'freq',
      sets = rev(sort(unique(unlist(strsplit(data$Samples, '&'))))),
      nsets = 70)
dev.off()
