# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)

# Read the data
data <- read.delim('input/mapping_stats.tsv', sep='\t')

# Extract numeric values from relevant columns
data <- data %>%
  mutate(Passing_filtering = as.numeric(sub(' .*', '', Passing_filtering)),
         All_mapped_reads = as.numeric(sub(' .*', '', All_mapped_reads)),
         Uniquely_mapped_reads = as.numeric(sub(' .*', '', Uniquely_mapped_reads)))

# Calculate additional columns
data <- data %>%
  mutate(Multi_mapping = All_mapped_reads - Uniquely_mapped_reads,
         Unmapped = Total_reads - All_mapped_reads,
         Filtered = Total_reads - Passing_filtering)

# Reshape data for plotting
plot_data <- data %>%
  pivot_longer(cols = c(Uniquely_mapped_reads, Multi_mapping, Unmapped, Filtered),
               names_to = 'Category', values_to = 'Reads')

# Create the plot
p <- ggplot(plot_data, aes(x = interaction(Tissue, Sample, Rep), y = Reads, fill = Category)) +
  geom_bar(stat = 'identity') +
  facet_wrap(~ Line) +
  theme_minimal() +
  labs(title = 'Mapping statistics for ChIP_demo samples',
       x = 'Sample',
       y = 'Read Counts') +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Save the plot
pdf('output/mapping_stats.pdf', width = 12, height = 10)
print(p)
dev.off()
