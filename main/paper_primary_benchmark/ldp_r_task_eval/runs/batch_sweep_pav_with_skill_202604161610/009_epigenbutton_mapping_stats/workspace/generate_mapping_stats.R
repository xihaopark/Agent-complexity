library(ggplot2)
library(dplyr)
library(tidyr)

# Read the data
data <- read.delim('input/mapping_stats.tsv', sep='\t')

# Extract numeric values from formatted columns
data <- data %>%
  mutate(
    Passing_filtering = as.numeric(sub(' .*', '', Passing_filtering)),
    All_mapped_reads = as.numeric(sub(' .*', '', All_mapped_reads)),
    Uniquely_mapped_reads = as.numeric(sub(' .*', '', Uniquely_mapped_reads))
  )

# Calculate additional columns
transformed_data <- data %>%
  mutate(
    Multi_mapping_reads = All_mapped_reads - Uniquely_mapped_reads,
    Unmapped_reads = Total_reads - All_mapped_reads,
    Filtered_reads = Total_reads - Passing_filtering
  )

# Prepare data for plotting
plot_data <- transformed_data %>%
  gather(key = "Type", value = "Count", Uniquely_mapped_reads, Multi_mapping_reads, Unmapped_reads, Filtered_reads)

# Create the plot
plot <- ggplot(plot_data, aes(x = interaction(Tissue, Sample, Rep), y = Count, fill = Type)) +
  geom_bar(stat = "identity") +
  facet_wrap(~ Line) +
  theme_minimal() +
  labs(title = "Mapping statistics for ChIP_demo samples", x = "Sample", y = "Read Count") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Save the plot
pdf("output/mapping_stats.pdf", width = 12, height = 10)
print(plot)
dev.off()
