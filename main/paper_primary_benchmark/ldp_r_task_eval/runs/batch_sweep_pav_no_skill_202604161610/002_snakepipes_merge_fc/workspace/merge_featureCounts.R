# Load necessary library
library(dplyr)

# Define file paths
files <- list(
  'sampleA' = 'input/sampleA.counts.txt',
  'sampleB' = 'input/sampleB.counts.txt',
  'sampleC' = 'input/sampleC.counts.txt'
)

# Read and merge data
merged_data <- NULL
for (sample_name in names(files)) {
  # Read the data
  data <- read.delim(files[[sample_name]], header = TRUE)
  
  # Select only Geneid and sample count
  data <- data %>% select(Geneid, sample_counts = 7)
  
  # Rename the sample count column
  colnames(data)[2] <- sample_name
  
  # Merge data
  if (is.null(merged_data)) {
    merged_data <- data
  } else {
    merged_data <- full_join(merged_data, data, by = 'Geneid')
  }
}

# Set Geneid as rownames and drop the column
rownames(merged_data) <- merged_data$Geneid
merged_data <- merged_data[ , -1]

# Write the output
write.table(merged_data, 'output/merged_counts.tsv', sep = '\t', quote = FALSE, col.names = NA)
