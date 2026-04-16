log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

library(here)
library(methylKit)
library(tidyverse)


#styler: off
INPUT_FILE              <- snakemake@input[[1]]
MIN_PER_GROUP           <- as.integer(snakemake@params$min_per_group)
DESTRAND                <- snakemake@params$destrand
USE_DB                  <- as.logical(snakemake@params$use_db)
THREADS                 <- snakemake@threads

DBPATH <- dirname(snakemake@output$dbfiles[[1]])
# styler: on

print(DBPATH)

mk_filt_norm <- readRDS(INPUT_FILE)


message("convert to DB object...")

mk_filt_norm_db <- methylKit::makeMethylDB(mk_filt_norm, dbdir = DBPATH)
message("done. ")
