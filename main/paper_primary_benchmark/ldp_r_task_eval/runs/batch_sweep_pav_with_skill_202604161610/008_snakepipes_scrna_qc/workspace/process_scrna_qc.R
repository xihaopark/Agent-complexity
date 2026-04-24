# Load necessary libraries
library(ggplot2)
library(dplyr)
library(tidyr)

# Function to read and process libsum files
process_libsum <- function(file_path) {
  data <- read.table(file_path, header = FALSE, sep = "\t")
  colnames(data) <- c("sample", "metric", "value", "pct")
  return(data)
}

# Function to read and process cellsum files
process_cellsum <- function(file_path) {
  data <- read.table(file_path, header = TRUE, sep = "\t")
  return(data)
}

# Read and process all libsum files
libsum_files <- list.files("input/qc", pattern = "*.libsum", full.names = TRUE)
libsum_data <- lapply(libsum_files, process_libsum)
libsum_combined <- do.call(rbind, libsum_data)

# Create wide tables for reads and percentages
libstats_reads <- libsum_combined %>%
  filter(metric == "total_reads" | metric == "mapped_reads" | metric == "unique_reads") %>%
  select(sample, metric, value) %>%
  spread(key = metric, value = value)

libstats_pct <- libsum_combined %>%
  filter(metric == "total_reads" | metric == "mapped_reads" | metric == "unique_reads") %>%
  select(sample, metric, pct) %>%
  spread(key = metric, value = pct)

# Write the wide tables to output
write.table(libstats_reads, "output/scrna_qc.libstats_reads.tsv", sep = "\t", row.names = FALSE)
write.table(libstats_pct, "output/scrna_qc.libstats_pct.tsv", sep = "\t", row.names = FALSE)

# Read and process all cellsum files
cellsum_files <- list.files("input/qc", pattern = "*.cellsum", full.names = TRUE)
cellsum_data <- lapply(cellsum_files, process_cellsum)

# Normalize reads/UMI per cell by per-sample sum * 1e6
normalize_cellsum <- function(data) {
  data <- data %>%
    group_by(sample) %>%
    mutate(norm_READS_UNIQFEAT = READS_UNIQFEAT / sum(READS_UNIQFEAT) * 1e6,
           norm_UMI = UMI / sum(UMI) * 1e6)
  return(data)
}

normalized_cellsum_data <- lapply(cellsum_data, normalize_cellsum)

# Generate plots
plot_reads_UMI <- function(data, output_file) {
  p <- ggplot(data, aes(x = norm_READS_UNIQFEAT, y = norm_UMI)) +
    geom_point() +
    theme_minimal() +
    ggtitle("Normalized Reads vs UMI")
  ggsave(output_file, plot = p)
}

# Apply plotting function to each normalized dataset
mapply(plot_reads_UMI, normalized_cellsum_data, paste0("output/scrna_qc.reads_UMI_plot", seq_along(normalized_cellsum_data), ".png"))
