# Load necessary library
library(dplyr)

# Read input files
data1 <- read.table('input/coutt/plate1_lib1.corrected.txt', header=TRUE, sep='\t')
data2 <- read.table('input/coutt/plate1_lib2.corrected.txt', header=TRUE, sep='\t')
data3 <- read.table('input/coutt/plate2_lib1.corrected.txt', header=TRUE, sep='\t')

# Merge data by GENEID with outer join
merged_data <- full_join(data1, data2, by='GENEID') %>%
  full_join(data3, by='GENEID')

# Prefix column names with source file basename
colnames(merged_data)[-1] <- paste0(rep(c('plate1_lib1_', 'plate1_lib2_', 'plate2_lib1_'), each=8), colnames(merged_data)[-1])

# Replace NA with 0
merged_data[is.na(merged_data)] <- 0

# Write merged data to output file
write.table(merged_data, 'output/merged_coutt.tsv', sep='\t', row.names=FALSE, quote=FALSE)

# Generate cell names table
cell_names <- data.frame(
  sample = rep(c('plate1_lib1', 'plate1_lib2', 'plate2_lib1'), each=8),
  plate = rep(c('plate1', 'plate1', 'plate2'), each=8),
  library = rep(c('lib1', 'lib2', 'lib1'), each=8),
  cell_idx = rep(1:8, 3),
  cell_name = colnames(merged_data)[-1]
)

# Write cell names table to output file
write.table(cell_names, 'output/merged_coutt.cell_names.tsv', sep='\t', row.names=FALSE, quote=FALSE)
