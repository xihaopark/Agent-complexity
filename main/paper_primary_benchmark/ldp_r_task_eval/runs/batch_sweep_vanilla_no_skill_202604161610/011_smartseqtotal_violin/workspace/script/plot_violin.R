library(ggplot2)
library(ggpubr)
library(dplyr)

# Load data
df_silhouette <- read.delim('cache/df_silhouette1012.tsv')
df_calinski <- read.delim('cache/df_calinski1012.tsv')
df_davies <- read.delim('cache/df_davies1012.tsv')

# Add a new column to identify the metric
df_silhouette$metric <- 'Silhouette'
df_calinski$metric <- 'Calinski-Harabasz'
df_davies$metric <- 'Davies-Bouldin'

# Combine all data frames
df_combined <- bind_rows(df_silhouette, df_calinski, df_davies)

# Plot
p <- ggplot(df_combined, aes(x=data_type, y=value, fill=data_type)) +
  geom_violin() +
  facet_wrap(~metric, scales='free') +
  scale_fill_brewer(palette='Set3') +
  theme_pubclean() +
  stat_compare_means(method='wilcox.test') +
  labs(title='Benchmark Scores', x='Data Type', y='Score')

# Save the plot
ggsave('output/violin_scores.png', plot=p, width=2400, height=1200, units='px')
