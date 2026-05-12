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
frip_scores <- tibble()
for (i in 1:length(data)) {
  frip_scores <- rbind(frip_scores, data[[i]])
}
names(frip_scores) <- c("sample_control", "frip")

frip <- ggplot(frip_scores, aes(x = sample_control, y = frip, fill = sample_control)) +
  geom_bar(stat="Identity", color="black") +
  theme_minimal() +
  labs(x="", y="FRiP score") +
  theme(legend.position = "right") +
  guides(fill=guide_legend("samples with controls")) +
  ggtitle("FRiP score")

ggsave(snakemake@output[[1]], frip)
