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


### load libraries
library("limma")
library("edgeR")
library("data.table")

### configs
set.seed(42)

# input
data_path <- snakemake@input[["filtered_counts"]]

# output
result_path <- snakemake@output[["normalized_counts"]]
plot_path <- snakemake@output[["voom_plot"]]

# parameters
split <- snakemake@params[["split"]]

# config
edgeR_parameters <- snakemake@config[["edgeR_parameters"]]
voom_parameters <- snakemake@config[["voom_parameters"]]

### load data
# data <- read.csv(file=file.path(data_path), row.names=1)
data <- data.frame(fread(file.path(data_path), header=TRUE), row.names=1, check.names=FALSE)

# calculate normalization factors (normalized library size factors) if configured
dge <- DGEList(data)
dge <- calcNormFactors(dge,
                       method = voom_parameters[["calcNormFactors_method"]],
                       refColumn = if(edgeR_parameters[["refColumn"]]!="NULL") edgeR_parameters[["refColumn"]] else NULL,
                       logratioTrim = edgeR_parameters[["logratioTrim"]],
                       sumTrim = edgeR_parameters[["sumTrim"]],
                       doWeighting = if(edgeR_parameters[["doWeighting"]]=="TRUE") TRUE else FALSE,
                       Acutoff = edgeR_parameters[["Acutoff"]],
                       p = edgeR_parameters[["p"]]
                      )

### normalize data using VOOM
png(plot_path, width = 4, height = 4, units = "in", res = 300)
voom_results <- voom(counts = dge,
                     design = NULL,
                     #lib.size = NULL,
                     normalize.method = voom_parameters[["normalize.method"]],
                     block = NULL,
                     correlation = NULL,
                     weights = NULL,
                     span = voom_parameters[["span"]],
                     plot = TRUE,
                     save.plot = FALSE
                    )
dev.off()

norm_data <- voom_results$E
    
# save normalized data
# write.csv(norm_data, file=file.path(result_path), row.names=TRUE)
fwrite(as.data.frame(norm_data), file=file.path(result_path), row.names=TRUE)
