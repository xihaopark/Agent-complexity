#' Load multiple RDS file containg MethylBase objects and converted to a unified
#' tibble.
#'
#' The returned tibble is stored as RDS file.

log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

source(file.path(snakemake@scriptdir, "methylkit_common.R"))
# styler: off
INPUT_FILES     <- snakemake@input$rds_list
OUTPUT_RDS      <- snakemake@output$rds
OUTPUT_TSV      <- snakemake@output$stats_tsv

# check if any of the input files is empty and remove from list if so
# print warning message indicating which files are empty
empty_files <- purrr::map_lgl(INPUT_FILES, function(x) file.size(x) == 0)
if (any(empty_files)) {
  message("Warning: The following input files are empty and will be ignored:")
  message(INPUT_FILES[empty_files])
  message("\n")
}

INPUT_FILES <- INPUT_FILES[!empty_files]

message("load data...")

mkobjs <- purrr::map(
  INPUT_FILES,
  readRDS
)

message("convert to tibble")
df_mku <- purrr::map(mkobjs, mku2tibble) |>
  purrr::list_rbind()

rm(mkobjs)

message("done")

message("rename samples and save data...")
df_mku |>
  # mutate(sample = stringr::str_replace(sample, "OENDES-MO", "OENDES-MO_02_2020-3Y42903")) |>
  # mutate(sample = stringr::str_replace(sample, "GR-GAL-2019-014-REF", "GR-GAL-2019-014")) |>
  # mutate(sample = stringr::str_replace(sample, "OEN-CYP-20e", "OEN_CYP-20e")) |>
  # mutate(sample = stringr::str_replace(sample, "Oencyp_black", "OEN_CYP-19e")) |>
  saveRDS(OUTPUT_RDS)


message("done")



df_mku |>
  tidyr::pivot_wider(id_cols = c("chr", "start", "sample"), names_from = "metric", values_from = value) |>
  filter(
    !is.na(numCs),
    !is.na(coverage),
    coverage != 0
  ) |>
  dplyr::mutate(mCpG = numCs / coverage) |>
  dplyr::group_by(sample, chr) |>
  dplyr::summarise(mean_mCpG = mean(mCpG), .groups = "keep") |>
  mutate(sample = stringr::str_replace(sample, "OENDES-MO", "OENDES-MO_02_2020-3Y42903")) |>
  mutate(sample = stringr::str_replace(sample, "GR-GAL-2019-014-REF", "GR-GAL-2019-014")) |>
  mutate(sample = stringr::str_replace(sample, "OEN-CYP-20e", "OEN_CYP-20e")) |>
  mutate(sample = stringr::str_replace(sample, "Oencyp_black", "OEN_CYP-19e")) |>
  readr::write_tsv(OUTPUT_TSV)
