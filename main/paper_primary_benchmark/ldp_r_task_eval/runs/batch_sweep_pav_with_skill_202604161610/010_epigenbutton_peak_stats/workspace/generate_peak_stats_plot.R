library(ggplot2)
library(dplyr)
library(tidyr)

# Read the data
data <- read.delim('input/peak_stats.tsv', sep='\t')

# Strip 'selected' from Selected_peaks
data$Selected_peaks <- as.numeric(gsub(' selected', '', data$Selected_peaks))

# Transform data for plotting
plot_data <- data %>%
  pivot_longer(cols = c('Selected_peaks', 'Peaks_in_Rep1', 'Peaks_in_Rep2', 'Peaks_in_merged', 'Peaks_in_pseudo_reps', 'Peaks_in_idr'),
               names_to = 'Stage', values_to = 'Peaks')

# Create the plot
p <- ggplot(plot_data, aes(x = Sample, y = Peaks, fill = Stage)) +
  geom_bar(stat = 'identity', position = 'dodge') +
  facet_wrap(~ Line + Tissue) +
  scale_fill_brewer(palette = 'Paired') +
  labs(title = 'Number of peaks in each ChIP sample of ChIP_demo') +
  theme_minimal()

# Save the plot
pdf('output/peak_stats.pdf', width = 10, height = 12)
print(p)
dev.off()
