# Load necessary libraries
library(ggplot2)

# Read the data
data <- read.table('input/peak_stats.tsv', header = TRUE, sep = '\t')

# Strip 'selected' from Selected_peaks and convert to numeric
data$Selected_peaks <- as.numeric(sub(' selected', '', data$Selected_peaks))

# Melt the data for ggplot
library(reshape2)
data_melted <- melt(data, id.vars = c('Line', 'Tissue', 'Sample'), 
                    measure.vars = c('Selected_peaks', 'Peaks_in_Rep1', 'Peaks_in_Rep2', 
                                     'Peaks_in_merged', 'Peaks_in_pseudo_reps', 'Peaks_in_idr'),
                    variable.name = 'Stage', value.name = 'Peaks')

# Create the plot
plot <- ggplot(data_melted, aes(x = Sample, y = Peaks, fill = Stage)) +
  geom_bar(stat = 'identity', position = 'dodge') +
  facet_wrap(~ Line + Tissue) +
  scale_fill_brewer(palette = 'Paired') +
  theme_minimal() +
  labs(title = 'Number of peaks in each ChIP sample of ChIP_demo',
       x = 'Sample',
       y = 'Number of Peaks')

# Save the plot
pdf('output/peak_stats.pdf', width = 10, height = 12)
print(plot)
dev.off()
