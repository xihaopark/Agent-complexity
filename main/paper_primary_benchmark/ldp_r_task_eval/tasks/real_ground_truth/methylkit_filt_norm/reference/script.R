log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

library(here)
library(methylKit)
library(tidyverse)
library(purrr)

source(file.path(snakemake@scriptdir, "methylkit_common.R"))

#styler: off
INPUT_FILE              <- snakemake@input[[1]]
LO_COV_THRESHOLD_ABS    <- snakemake@params$low_cov_threshold_abs
HI_COV_THRESHOLD_PERC   <- snakemake@params$high_cov_threshold_perc
OUTPUT_RDS              <- snakemake@output$rds
OUTPUT_PLOTS_FILT       <- dirname(snakemake@output$plots_filt)
OUTPUT_PLOTS_NORM       <- dirname(snakemake@output$plots_norm)
# styler: on
mk_raw <- readRDS(INPUT_FILE)

mk_filt <- methylKit::filterByCoverage(
  mk_raw,
  lo.count = LO_COV_THRESHOLD_ABS,
  lo.perc  = NULL,
  hi.count = NULL,
  hi.perc  = HI_COV_THRESHOLD_PERC
)

mk_filt_norm <- methylKit::normalizeCoverage(
  mk_filt,
  method = "median"
)

saveRDS(mk_filt_norm, OUTPUT_RDS)

stats <- purrr::map(
  1:length(mk_filt_norm),
  function(i) sample_meth_stats(mk_filt_norm[[i]])
) |> list_rbind()

write_tsv(stats, snakemake@output$stats_tsv)

sink()
