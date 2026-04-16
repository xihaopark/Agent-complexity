log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

suppressPackageStartupMessages(require(DSS))
suppressPackageStartupMessages(require(bsseq))
suppressPackageStartupMessages(library(here))
suppressPackageStartupMessages(library(tidyverse))

source(file.path(snakemake@scriptdir, "load_metadata.R"))
source(file.path(snakemake@scriptdir, "methylkit_common.R"))

#styler: off
INPUT_FILE                 <- snakemake@input$df
METADATA_FILE              <- snakemake@input$sample_metadata
SPECIES_COLORS_FILE        <- snakemake@input$colors_file
SPECIES_METADATA_FILE      <- snakemake@input$species_metadata
OUTPUT_PLOTS               <- snakemake@output$plots
OUTPUT_TSV_DML             <- snakemake@output$tsv_dml
OUTPUT_TSV_DMR             <- snakemake@output$tsv_dmr
# SAMPLE_NAMES               <- as.list(snakemake@params$samples)
GROUP1_SPECIES             <- as.character(snakemake@params$group1)
GROUP2_SPECIES             <- as.character(snakemake@params$group2)

GROUP1_SAMPLES             <- as.character(snakemake@params$group1)
GROUP2_SAMPLES             <- as.character(snakemake@params$group2)
# styler: on

# are groups provided as sample labels or as species?
if ("groups_by_samples" %in% names(snakemake@params)) {
  GROUPS_BY_SAMPLES <- as.logical(snakemake@params$groups_by_samples)
} else {
  GROUPS_BY_SAMPLES <- FALSE
}

SPECIES_METADATA <-
  readr::read_tsv(SPECIES_METADATA_FILE) |>
  readr::type_convert()

METADATA <- load_metadata(
  fpath = METADATA_FILE,
  species_metadata = SPECIES_METADATA
)

colors <- readr::read_tsv(SPECIES_COLORS_FILE) |>
  dplyr::select(c(species, color)) |>
  tibble::deframe()


df_mku <- readRDS(INPUT_FILE) |>
  mutate(sample = str_remove(sample, ".bismark.cov.gz"))

samples <- df_mku$sample |> unique()


# functions
get_samples_by_species <- function(df, species) {
  stopifnot(species %in% df$Species)

  print(species)
  df |>
    dplyr::select(c(Species, sample)) |>
    dplyr::filter(sample %in% bsseq::sampleNames(BSobj)) |>
    dplyr::filter(Species %in% species) |>
    dplyr::pull(sample)
}

df_prepare_for_DSS <- function(df, sample_label) {
  df |>
    # dplyr::filter(stringr::str_starts(chr, "chr")) |>  # not need if done per chromosome
    dplyr::filter(sample == sample_label) |>
    tidyr::pivot_wider(
      id_cols = c("chr", "start"),
      names_from = "metric", values_from = "value"
    ) |>
    dplyr::rename(
      pos = start,
      N = coverage,
      X = numCs
    ) |>
    dplyr::select(c(chr, pos, N, X))
}

# define groups

if (GROUPS_BY_SAMPLES) {
  .group1 <- GROUP1_SAMPLES
  .group2 <- GROUP2_SAMPLES
} else {
  .group1 <- get_samples_by_species(METADATA, GROUP1_SPECIES)
  .group2 <- get_samples_by_species(METADATA, GROUP2_SPECIES)
}

message(paste0("group 1 ", .group1))
message(paste0("group 2 ", .group2))


# only select samples in groups

samples <- c(.group1, .group2)

# routine

message("load data...")
list_bsseq <- purrr::map(
  samples,
  ~ df_prepare_for_DSS(df_mku, .x)
)
message("done. ")

message("converting to BSseq object ...")
BSobj <- DSS::makeBSseqData(
  dat = list_bsseq,
  sampleNames = samples
)
message("done")

if (GROUPS_BY_SAMPLES) {
  .group1 <- GROUP1_SAMPLES
  .group2 <- GROUP2_SAMPLES
} else {
  .group1 <- get_samples_by_species(METADATA, GROUP1_SPECIES)
  .group2 <- get_samples_by_species(METADATA, GROUP2_SPECIES)
}

message(paste0("group 1 ", .group1))
message(paste0("group 2 ", .group2))

# check both groups contain samples
stopifnot(all(purrr::map(list(.group1, .group2), ~ length(.x) > 1)))

if (length(setdiff(.group1, samples) > 0)) message(paste0("missing samples in group 1 ", setdiff(.group1, samples)))
if (length(setdiff(.group2, samples) > 0)) message(paste0("missing samples in group 2 ", setdiff(.group2, samples)))


dmlTest.sm <- DSS::DMLtest(BSobj,
  group1 = .group1,
  group2 = .group2,
  smoothing = TRUE, ncores = 4
)



dmls <- callDML(dmlTest.sm, p.threshold = 0.001)
message(paste0("start writing to: ", OUTPUT_TSV_DML))
write_tsv(dmls, file = OUTPUT_TSV_DML)
message("done. ")

dmrs_raw <- DSS::callDMR(dmlTest.sm, p.threshold = 0.01)

if (length(dmrs_raw) == 0) {
  write_tsv(data.frame(), file = OUTPUT_TSV_DMR)
  message("no DMRs found. ")
  pdf(file = OUTPUT_PLOTS, width = 10, height = 20)
  # do not plot if no DMRs were found
  dev.off()
} else {
  dmrs <- dmrs_raw |>
    mutate(comparison = paste0(paste0(GROUP1_SPECIES, collapse = ","), " : ", paste0(GROUP2_SPECIES, collapse = ",")))

  message(paste0("start writing to: ", OUTPUT_TSV_DMR))
  write_tsv(dmrs, file = OUTPUT_TSV_DMR)
  message("done. ")

  message(paste0("start plottings to: ", OUTPUT_PLOTS))

  par(mar = c(1, 1, 1, 1))
  pdf(file = OUTPUT_PLOTS, width = 30, height = 100)
  # do not plot if no DMRs were found
  DSS::showOneDMR(dmrs[1, ], BSobj, ext = 100)
  purrr::map(
    1:nrow(dmrs),
    function(i) showOneDMR(dmrs[i, ], BSobj)
  )
  dev.off()
  message("done. ")
}
