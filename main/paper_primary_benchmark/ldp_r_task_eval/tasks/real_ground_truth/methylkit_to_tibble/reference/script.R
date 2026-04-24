log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

#styler: off
INPUT_FILE <- snakemake@input$rds
OUTPUT_RDS <- snakemake@output$rds
OUTPUT_TSV <- snakemake@output$stats_tsv
# styler: on

mku2tibble <- function(mku_obj) {
  suppressPackageStartupMessages(require(tidyr))
  suppressPackageStartupMessages(require(dplyr))

  sample_names <- mku_obj@sample.ids |>
    tibble::enframe(name = "sample_num", value = "sample")

  print(getwd())
  if (!is.na(mku_obj@dbpath)) {
    mku_obj <- methylKit::getData(mku_obj)
  }

  mku_obj |>
    as_tibble() |>
    dplyr::select(-matches("numTs")) |>
    tidyr::pivot_longer(
      cols = matches("coverage|numCs"),
      names_to = c("metric", "sample"),
      names_pattern = "([A-Za-z]*)([0-9]{1,2})",
      values_to = "value"
    ) |>
    drop_na() |>
    dplyr::mutate(sample = as.integer(sample)) |>
    dplyr::left_join(sample_names, by = c("sample" = "sample_num")) |>
    dplyr::select(-sample) |>
    dplyr::rename(sample = "sample.y")
}



if (stringr::str_ends(INPUT_FILE, ".rds")) {
  mku <- readRDS(INPUT_FILE)
} else if (stringr::str_ends(INPUT_FILE, ".txt.bgz")) {
  cat(paste0("loading mku from ", INPUT_FILE))
  mku <- methylKit::readMethylDB(INPUT_FILE)
  mku <- as(mku, "methylBase")
}

# samplename replacements
mku@sample.ids <- stringr::str_replace(mku@sample.ids, "OENDES-MO", "OENDES-MO_02_2020-3Y42903")
mku@sample.ids <- stringr::str_replace(mku@sample.ids, "GR-GAL-2019-014-REF", "GR-GAL-2019-014")
mku@sample.ids <- stringr::str_replace(mku@sample.ids, "OEN-CYP-20e", "OEN_CYP-20e")
mku@sample.ids <- stringr::str_replace(mku@sample.ids, "Oencyp_black", "OEN_CYP-19e")

df_mku <- mku2tibble(mku) # |> left_join(METADATA)

saveRDS(df_mku, OUTPUT_RDS)

df_mku |>
  tidyr::pivot_wider(id_cols = c("chr", "start", "sample"), names_from = "metric", values_from = value) |>
  dplyr::mutate(mCpG = numCs / coverage) |>
  dplyr::group_by(sample, chr) |>
  dplyr::summarise(mean_mCpG = mean(mCpG), .groups = "keep") |>
  readr::write_tsv(OUTPUT_TSV)
