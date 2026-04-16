#' Load Metadata from CSV and Process
#'
#' This function loads metadata from a CSV file located at the given file path (fpath) and processes it based on the provided parameters.
#'
#' @param fpath File path to the CSV file containing the metadata.
#' @param species_metadata A data frame containing metadata for different species, with at least the columns 'scientific_name' and other species-specific information.
#' @param show_col_types Logical value indicating whether to show column types when reading the CSV file using the read_csv function from the readr package.
#'   The default value is FALSE.
#' @param subset Character vector of sample names to be used for subsetting the resulting data frame (df).
#'   If not provided, the function will keep all rows from the CSV file in the resulting data frame.
#' @return A processed data frame (df) containing the loaded metadata and additional information merged from the 'species_metadata' data frame.
#'
#' @import tibble
#' @import readr
#' @import dplyr
#' @import stringr
#'
#' @examples
#' # Assuming 'metadata.csv' contains the metadata and 'species_info' is a data frame with species-specific information
#' metadata <- load_metadata("metadata.csv", species_info, show_col_types = TRUE, subset = sample_names)
#'
#' @export
load_metadata <- function(fpath, species_metadata, show_col_types = FALSE, subset = NULL) {
  require(readr)

  # attempt to fix any encoding issues and abbreviate the genus
  species_metadata <- species_metadata |>
    dplyr::mutate(scientific_name = stringi::stri_enc_toutf8(stringr::str_replace(scientific_name, "Oenanthe[[:space:]]", "O. ")))

  # get the levels for correct ordering
  species_levels <- levels(reorder(species_metadata$scientific_name, species_metadata$species_order))

  df <- readr::read_tsv(fpath, show_col_types = show_col_types, trim_ws = TRUE) |>
    # rename samples and Species columns
    # abbreviate genus
    dplyr::mutate(Species = stringr::str_replace_all(Species, "Oenanthe", "O.")) |>
    # replace any mis-formated or mis-encoded spaces
    dplyr::mutate(Species = stringr::str_replace_all(Species, "[[:space:]]+", " ")) |>
    # remove question marks in all columns
    dplyr::mutate(across(everything(), ~ stringr::str_remove(.x, "\\?"))) -> df

  .nrow_metadata <- nrow(df)


  df |>
    dplyr::filter(!Species %in% species_levels) -> df_excluded

  df |>
    dplyr::filter(Species %in% species_levels) -> df


  if (nrow(df) != .nrow_metadata) {
    message(glue::glue("[ WARNING ] Number of metadata rows changed, is now {nrow(df)} and was {.nrow_metadata}."))
    message("\nThe following metadata rows were excluded: \n")
    message(paste("\n - ", sort(unique(df_excluded$Species))), "\n")
  }

  df |>
    dplyr::mutate(Species = dplyr::case_when(
      stringr::str_detect(Species, "^O. pleschanka$") ~ "O. pleschanka",
      stringr::str_detect(Species, "^O. melanoleuca$") ~ "O. melanoleuca",
      stringr::str_detect(Species, ".*melanoleuca x pleschanka.*") ~ "O. melanoleuca x pleschanka",
      .default = as.character(Species)
    )) |>
    # sort Species by converting to factor
    dplyr::mutate(
      Species = forcats::fct(
        Species,
        levels = species_levels
      )
    ) |>
    dplyr::left_join(species_metadata,
      by = c("Species" = "scientific_name")
    ) |>
    # convert decimal coordinates (longi/lati-tude_dec) to intergers
    dplyr::mutate(across(contains("tude_dec"), as.integer)) ->
  df


  df |>
    dplyr::filter(is.na(species_order)) |>
    dplyr::pull(Species) |>
    unique()

  if (!is.null(subset)) {
    sample_numbers <-
      tibble::tibble(sample = subset) |>
      tibble::rownames_to_column("sample_num")

    df |>
      dplyr::inner_join(sample_numbers) -> df
  }

  return(df)
}
