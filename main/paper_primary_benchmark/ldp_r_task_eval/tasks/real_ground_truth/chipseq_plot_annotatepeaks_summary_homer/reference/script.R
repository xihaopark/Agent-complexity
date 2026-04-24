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

homer_data <- read_tsv(snakemake@input[[1]])
homer_data <- homer_data %>% gather(`exon`, `Intergenic`, `intron`, `promoter-TSS`, `TTS`, key="sequence_element", value="counts")

peaks_sum <- ggplot(homer_data, aes(x = counts, y = sample, fill = sequence_element)) +
  geom_bar(position="fill", stat="Identity") +
  theme_minimal() +
  labs(x="", y="Peak count") +
  theme(legend.position = "right") +
  guides(fill=guide_legend("sequence element")) +
  ggtitle("Peak to feature proportion")

ggsave(snakemake@output[[1]], peaks_sum)

