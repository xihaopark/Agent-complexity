log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

library(here)
library(methylKit)
library(tidyverse)


#styler: off
INPUT_FILES              <- snakemake@input[[1]]
OUTPUT_RDS              <- snakemake@output$rds
MIN_PER_GROUP           <- as.integer(snakemake@params$min_per_group)
DESTRAND                <- snakemake@params$destrand
USE_DB                  <- as.logical(snakemake@params$use_db)
THREADS                 <- snakemake@threads

DBPATH <- dirname(snakemake@output$db_file)
# styler: on

mk_filt_norm <- readRDS(INPUT_FILE)

message("loaded methylkit object")

if (USE_DB) {
  mk_united <- methylKit::unite(
    mk_filt_norm_db,
    destrand = DESTRAND,
    min.per.group = MIN_PER_GROUP,
    mc.cores = 8,
    save.db = TRUE,
    chunk.size = 1e6,
    dbdir = DBPATH,
    suffix = "unite"
  )
} else {
  mk_united <- methylKit::unite(
    mk_filt_norm,
    destrand = DESTRAND,
    min.per.group = MIN_PER_GROUP,
    mc.cores = THREADS
  )
}

saveRDS(mk_united, OUTPUT_RDS)

stats <-
  tibble(
    n_samples = length(methylKit::getSampleID(mk_united)),
    n_sites = methylKit::getData(mk_united) |> nrow(),
    min_per_group = MIN_PER_GROUP,
    destrand = DESTRAND,
    use_db = USE_DB,
    db_path = DBPATH
  )

write_tsv(stats, snakemake@output$stats_tsv)
