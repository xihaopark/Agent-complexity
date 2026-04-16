log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

source(file.path(snakemake@scriptdir, "methylkit_common.R"))

suppressPackageStartupMessages(library(here))
suppressPackageStartupMessages(library(methylKit))
suppressPackageStartupMessages(library(tidyverse))


INPUT_FILES <- snakemake@input$dbfiles
INPUT_REPEATMASK_GTF <- snakemake@input$rm_gtf
OUTPUT_RDS <- snakemake@output$rds
OUTPUT_TIBBLE <- snakemake@output$tibble
CHR_LIST <- snakemake@wildcards$chr
MIN_PER_GROUP <- as.integer(snakemake@params$min_per_group)
DESTRAND <- snakemake@params$destrand

EXCLUDE_SAMPLES <- snakemake@params$exclude


for (samplename in EXCLUDE_SAMPLES) {
  message(paste0("exclude : ", samplename))
  INPUT_FILES <- unlist(purrr::map(INPUT_FILES, ~ purrr::discard(.x, str_detect(.x, samplename))))
}

message(paste0("included sample count: ", length(INPUT_FILES)))


mk_recreated <- purrr::map(
  INPUT_FILES,
  function(infile) {
    mk <- methylKit::readMethylDB(infile)
    rows <- which(methylKit::getData(mk)$chr %in% CHR_LIST)
    methylKit::select(mk, rows)
  }
)

mk_recreated2 <- methylKit::methylRawList(
  mk_recreated,
  treatment = rep(c(0), length(mk_recreated))
)


mk_united <- methylKit::unite(mk_recreated2,
  destrand = DESTRAND,
  min.per.group = MIN_PER_GROUP,
  mc.cores = 8
)


saveRDS(mk_united, OUTPUT_RDS)

saveRDS(mku2tibble(mk_united), OUTPUT_TIBBLE)


stats <-
  tibble(
    n_samples = length(methylKit::getSampleID(mk_united)),
    n_sites = methylKit::getData(mk_united) |> nrow(),
    min_per_group = MIN_PER_GROUP,
    destrand = DESTRAND,
    use_db = "FALSE",
    db_path = "NA"
  )

write_tsv(stats, snakemake@output$stats_tsv)
