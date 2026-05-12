# V3 device-redirect prelude (injected) ----------------------------------------
local({
  .orig_pdf  <- grDevices::pdf
  .orig_png  <- grDevices::png
  .orig_svg  <- grDevices::svg
  .orig_jpeg <- grDevices::jpeg
  assign('pdf',  function(file = NA, ...)     .orig_pdf(file = tempfile(fileext = '.pdf'), ...), envir = globalenv())
  assign('png',  function(filename = NA, ...) .orig_png(filename = tempfile(fileext = '.png'), ...), envir = globalenv())
  assign('svg',  function(filename = NA, ...) .orig_svg(filename = tempfile(fileext = '.svg'), ...), envir = globalenv())
  assign('jpeg', function(filename = NA, ...) .orig_jpeg(filename = tempfile(fileext = '.jpg'), ...), envir = globalenv())
  assign('ggsave', function(filename, ...) invisible(NULL), envir = globalenv())
})
# ------------------------------------------------------------------------------

log <- file(snakemake@log[[1]], open="wt")
sink(log)
sink(log, type="message")

library("tidyverse")

data <- lapply(snakemake@input, read.table, header=F, stringsAsFactors = F)
counts <- tibble()
for (i in 1:length(data)) {
  counts <- rbind(counts, data[[i]])
}
names(counts) <- c("sample_control", "count")

peaks_counts <- ggplot(counts, aes(x = count, y = sample_control, fill=sample_control)) +
  geom_bar(stat="Identity", color="black") +
  theme_minimal() +
  labs(x="Peak count", y="") +
  theme(legend.position = "right") +
  guides(fill=guide_legend("samples with controls")) +
  ggtitle("Total peak count")

ggsave(snakemake@output[[1]], peaks_counts)
