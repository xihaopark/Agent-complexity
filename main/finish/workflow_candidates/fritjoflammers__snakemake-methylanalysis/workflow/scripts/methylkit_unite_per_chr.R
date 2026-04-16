log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

source(file.path(snakemake@scriptdir, "methylkit_common.R"))

suppressPackageStartupMessages(library(here))
suppressPackageStartupMessages(library(methylKit))
suppressPackageStartupMessages(library(tidyverse))

# styler: off.
INPUT_FILES <- snakemake@input$dbfiles
OUTPUT_RDS <- snakemake@output$rds
OUTPUT_TIBBLE <- snakemake@output$tibble
CHR_LIST <- snakemake@wildcards$chr
MIN_PER_GROUP <- as.integer(snakemake@params$min_per_group)
DESTRAND <- snakemake@params$destrand
# styler: on

EXCLUDE_SAMPLES <- snakemake@params$exclude


for (samplename in EXCLUDE_SAMPLES) {
  message(paste0("attempting to exclude : ", samplename))
  if (!any(purrr::map_lgl(INPUT_FILES, ~ str_detect(.x, samplename)))) {
    message(paste0("sample not found: ", samplename))
    next
  }
  INPUT_FILES <- unlist(purrr::map(INPUT_FILES, ~ purrr::discard(.x, str_detect(.x, samplename))))
  message(paste0("sample excluded: ", samplename))
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

n_samples <- length(INPUT_FILES)

mk_recreated2 <- methylKit::methylRawList(
  mk_recreated,
  treatment = rep(c(0), n_samples)
)

if (MIN_PER_GROUP > n_samples) {
  message("WARNING: MIN_PER_GROUP is larger than the number of samples. Setting MIN_PER_GROUP to the number of samples: ", n_samples)
  MIN_PER_GROUP <- n_samples
}

mk_united <- tryCatch(
  {
    methylKit::unite(mk_recreated2,
      destrand = DESTRAND,
      min.per.group = MIN_PER_GROUP,
      mc.cores = 8
    )
  },
  warning = function(war) {
    # warning handler picks up where error was generated
    print(paste("united caused WARNING:  ", war))
    return(NULL)
  },
  error = function(err) {
    # error handler picks up where error was generated
    print(paste("uniting caused error:  ", err))
    return(NULL)
  }
)

if (is.null(mk_united)) {
  n_sites <- 0
  # uniting failed, create empty files and exit
  cat(NULL, file = OUTPUT_RDS)
  cat(NULL, file = OUTPUT_TIBBLE)
} else {
  n_sites <- methylKit::getData(mk_united) |> nrow()
  saveRDS(mk_united, OUTPUT_RDS)
  saveRDS(mku2tibble(mk_united), OUTPUT_TIBBLE)
}

# write stats
stats <-
  tibble(
    n_samples = n_samples,
    n_sites = n_sites,
    min_per_group = MIN_PER_GROUP,
    destrand = DESTRAND,
    use_db = "FALSE",
    db_path = "NA"
  )

write_tsv(stats, snakemake@output$stats_tsv)
