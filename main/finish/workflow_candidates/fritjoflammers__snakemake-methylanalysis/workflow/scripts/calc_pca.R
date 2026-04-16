#' Calculate Principal Component Analysis (PCA) on Methylation Data
#'
#' This function performs Principal Component Analysis (PCA) on methylation data to reduce the dimensionality and cluster samples based on their methylation profiles.
#'
#' @param data A data object containing methylation data. It can be either a `methylBaseDB` object from the methylKit package or a data frame.
#' @param metadata A data frame containing metadata associated with the samples in the methylation data.
#' @param variance Logical value indicating whether to calculate the variance explained by each principal component.
#'   If TRUE, the function returns a data frame with the variance explained; if FALSE, it returns a data frame with PCA results.
#'   The default value is FALSE.
#' @return If variance is TRUE, a data frame containing the variance explained by each principal component.
#'   If variance is FALSE, a data frame containing PCA results with samples as rows and principal components as columns, along with the associated metadata.
#'
#' @import methylKit
#' @import dplyr
#' @import tidyr
#' @import tibble
#'
#' @examples
#' # Assuming 'methylation_data' is a data frame containing methylation data and 'sample_metadata' is a data frame containing metadata
#' pca_results <- calc_PCA(methylation_data, sample_metadata)
#' variance_explained <- calc_PCA(methylation_data, sample_metadata, variance = TRUE)
#'
#' @export
calc_PCA <- function(data, metadata = NULL, variance = FALSE, impute = FALSE) {
  require(dplyr)
  require(tidyr)
  require(tibble)
  require(pcaMethods)

  # set metadata
  if (is.null(metadata)) {
    metadata <- data |> dplyr::select(c(sample, Species))
  }

  if (any(class(data) %in% c("methylBaseDB", "methylBase"))) {
    mx_mCpG <- methylKit::percMethylation(mku)
    mx_mCpG <- na.omit(mx_mCpG) |>
      removeConstantColumns()

    # print error if impute is TRUE
    if (impute) {
      cat("Imputation is not supported for methylKit objects. Please use a data frame instead.")
    }
  } else if (any(class(data) == "data.frame")) {
    if ("perc_mCpG" %in% colnames(data)) {
      # rename seqnames column to chr
      data <- data |> rename_with(function(x) "chr", tidyr::matches("seqnames"))

      mx_mCpG <- data |>
        dplyr::select(chr, start, sample, perc_mCpG) |>
        tidyr::pivot_wider(names_from = sample, values_from = "perc_mCpG") |>
        dplyr::select(-c("chr", "start"))
    } else if ("metric" %in% colnames(data)) {
      mx_mCpG <- data |>
        tidyr::pivot_wider(id_cols = c("sample", "chr", "start"), names_from = c("metric"), values_from = "value") |>
        dplyr::mutate(perc_mCpG = numCs / coverage) |>
        dplyr::select(chr, start, sample, perc_mCpG) |>
        pivot_wider(names_from = sample, values_from = "perc_mCpG") |>
        dplyr::select(-c(chr, start))
    } else {
      return(NULL)
    }
  }

  # Perform PCA
  if (impute) {
    pca <- pcaMethods::pca(
      mx_mCpG |> data.matrix() |> t(),
      method = "nipals",
      scale = "uv",
      center = T,
      nPcs = 5
    )

    df_pca <- pca@scores |>
      as.data.frame() |>
      rownames_to_column("sample") |>
      left_join(metadata)

    if (variance) {
      var_explained <- pca@R2
      df_var <- tibble(
        comp = 1:length(var_explained),
        var_explained = var_explained
      )
      return(df_var)
    }
    # count occurences of TRUE values in pca@missing per columns
    rowSums(pca@missing) |> enframe()
  } else {
    pca <- prcomp(mx_mCpG, scale = TRUE)

    if (variance) {
      var_explained <- pca$sdev^2 / sum(pca$sdev^2)
      df_var <- tibble(
        comp = 1:length(var_explained),
        var_explained = var_explained
      )
      return(df_var)
    }

    df_pca <- pca$rotation |>
      as_tibble(rownames = "sample") |>
      dplyr::left_join(metadata)
  }

  return(df_pca)
}

# This function checks for and removes constant columns (with zero variance) from a dataset.
# It prints the number of constant columns found and their names (if any) to standard output.
#
# Args:
#   data: A data frame or matrix from which constant columns are to be removed.
#
# Returns:
#   A list containing the cleaned data without constant columns and the names of the removed columns.
removeConstantColumns <- function(data) {
  # Calculate variance for each column
  variances <- apply(data, 2, var)

  # Identify columns with zero variance
  constant_columns <- which(variances == 0)

  # Report the number of constant columns
  cat("Number of constant columns found:", length(constant_columns), "\n")

  # If there are constant columns, print their names
  if (length(constant_columns) > 0) {
    cat("Names of constant columns:", names(data)[constant_columns], "\n")
    # Remove constant columns from the dataset
    data_clean <- data[, -constant_columns]
  } else {
    data_clean <- data
  }


  # Return the cleaned data and names of the removed columns
  return(list(cleaned_data = data_clean, removed_columns = names(data)[constant_columns]))
}
