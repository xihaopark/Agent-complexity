library(ggplot2)
library(ggpubr)
library(dplyr)

# Read data
df_silhouette <- read.csv('cache/df_silhouette1012.tsv', sep='\t')
df_calinski <- read.csv('cache/df_calinski1012.tsv', sep='\t')
df_davies <- read.csv('cache/df_davies1012.tsv', sep='\t')

# Add metric column
df_silhouette$metric <- 'Silhouette'
df_calinski$metric <- 'Calinski-Harabasz'
df_davies$metric <- 'Davies-Bouldin'

# Combine data
df_combined <- bind_rows(df_silhouette, df_calinski, df_davies)

# Filter data
df_combined <- df_combined %>% filter(down == 0.5)

# Plot
g <- ggplot(df_combined, aes(x=data_type, y=value, fill=data_type)) +
  geom_violin() +
  facet_wrap(~metric, scales='free') +
  scale_fill_brewer(palette='Set3') +
  stat_compare_means(method='wilcox.test') +
  theme_pubclean()

# Save plot
ggsave('output/violin_scores.png', plot=g, width=2400, height=1200, units='px')
