library(ggplot2)
library(dplyr)
library(tidyr)

# Read the data
data <- read.table('input/mapping_stats.tsv', header = TRUE, sep = '\t')

# Extract numeric values from the columns
extract_numeric <- function(x) {
  as.numeric(sub(' .*', '', x))
}

data <- data %>%
  mutate(
    Total_reads = as.numeric(Total_reads),
    Passing_filtering = extract_numeric(Passing_filtering),
    All_mapped_reads = extract_numeric(All_mapped_reads),
    Uniquely_mapped_reads = extract_numeric(Uniquely_mapped_reads),
    Multi_mapping = All_mapped_reads - Uniquely_mapped_reads,
    Unmapped = Passing_filtering - All_mapped_reads,
    Filtered = Total_reads - Passing_filtering
  )

# Reshape data for plotting
plot_data <- data %>%
  select(Line, Tissue, Sample, Rep, Uniquely_mapped_reads, Multi_mapping, Unmapped, Filtered) %>%
  pivot_longer(cols = c(Uniquely_mapped_reads, Multi_mapping, Unmapped, Filtered), names_to = 'Category', values_to = 'Reads')

# Create the plot
p <- ggplot(plot_data, aes(x = interaction(Tissue, Sample, Rep), y = Reads, fill = Category)) +
  geom_bar(stat = 'identity', position = 'stack') +
  facet_wrap(~ Line) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(title = 'Mapping statistics for ChIP_demo samples', x = 'Sample', y = 'Read Counts')

# Save the plot
pdf('output/mapping_stats.pdf', width = 12, height = 10)
print(p)
dev.off()
