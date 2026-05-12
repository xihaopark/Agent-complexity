# Load necessary libraries
library(ggplot2)
library(reshape2)

# Define function to read and process libsum files
process_libsum <- function(file_path) {
  data <- read.table(file_path, header = FALSE, sep = "\t")
  colnames(data) <- c("sample", "metric", "value", "pct")
  return(data)
}

# Define function to read and process cellsum files
process_cellsum <- function(file_path) {
  data <- read.table(file_path, header = TRUE, sep = "\t")
  return(data)
}

# Read all libsum files
libsum_files <- list.files(path = "input/qc/", pattern = "*.libsum", full.names = TRUE)
libsum_data <- do.call(rbind, lapply(libsum_files, process_libsum))

# Read all cellsum files
cellsum_files <- list.files(path = "input/qc/", pattern = "*.cellsum", full.names = TRUE)
cellsum_data <- do.call(rbind, lapply(cellsum_files, process_cellsum))

# Create wide tables for reads and percentages
libstats_reads <- dcast(libsum_data, sample ~ metric, value.var = "value")
libstats_pct <- dcast(libsum_data, sample ~ metric, value.var = "pct")

# Write the wide tables to TSV files
write.table(libstats_reads, "output/scrna_qc.libstats_reads.tsv", sep = "\t", row.names = FALSE)
write.table(libstats_pct, "output/scrna_qc.libstats_pct.tsv", sep = "\t", row.names = FALSE)

# Normalize reads/UMI per cell by per-sample sum * 1e6
cellsum_data$READS_UNIQFEAT_norm <- ave(cellsum_data$READS_UNIQFEAT, cellsum_data$sample, FUN = function(x) x / sum(x) * 1e6)
cellsum_data$UMI_norm <- ave(cellsum_data$UMI, cellsum_data$sample, FUN = function(x) x / sum(x) * 1e6)

# Generate z-score heatmaps and render PNGs
# Example for reads_UMI_plot
png("output/scrna_qc.reads_UMI_plot.png")
ggplot(cellsum_data, aes(x = factor(cell_idx), y = sample, fill = READS_UNIQFEAT_norm)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "red") +
  theme_minimal() +
  labs(title = "Reads UMI Plot", x = "Cell Index", y = "Sample")
dev.off()

# Additional plots can be generated similarly for other PNGs
# Plate cUPM
png("output/scrna_qc.plate_cUPM.png")
ggplot(cellsum_data, aes(x = factor(cell_idx), y = sample, fill = UMI_norm)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "blue") +
  theme_minimal() +
  labs(title = "Plate cUPM", x = "Cell Index", y = "Sample")
dev.off()

# Plate cRPM
png("output/scrna_qc.plate_cRPM.png")
ggplot(cellsum_data, aes(x = factor(cell_idx), y = sample, fill = READS_UNIQFEAT_norm)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "green") +
  theme_minimal() +
  labs(title = "Plate cRPM", x = "Cell Index", y = "Sample")
dev.off()

# Plate absolute transcripts
png("output/scrna_qc.plate_abs_transcripts.png")
ggplot(cellsum_data, aes(x = factor(cell_idx), y = sample, fill = READS_UNIQFEAT)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "purple") +
  theme_minimal() +
  labs(title = "Plate Absolute Transcripts", x = "Cell Index", y = "Sample")
dev.off()
