log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

plot_methylkit_histograms <- function(dat, output_dir, format = "pdf") {
  samples <- methylKit::getSampleID(dat)

  for (i in seq_along(samples)) {
    sample <- samples[i]

    # allow creation of PDF or SVG files
    if (format == "pdf") {
      pdf(file.path(output_dir, paste0(sample, ".pdf")))
    } else if (format == "svg") {
      svg(file.path(output_dir, paste0(sample, ".svg")))
    } else {
      stop("Invalid format argument. Must be 'pdf' or 'svg'.")
    }

    methylKit::getMethylationStats(
      dat[[i]],
      plot = TRUE,
      both.strands = FALSE
    )

    methylKit::getCoverageStats(
      dat[[i]],
      plot = TRUE,
      both.strands = FALSE
    )

    dev.off()
  }
}


#' Calculate methylation statistics for a methylKit object
#'
#' This function takes a methylKit object as input and calculates basic methylation statistics
#' including the sample name, the number of CpGs, and the mean methylation percentage.
#'
#' @param mkRawObj A methylKit object.
#'
#' @return A tibble (data frame) with columns:
#'   \describe{
#'     \item{sample}{Sample name extracted from the methylKit object.}
#'     \item{n_CpGs}{The total number of CpGs in the methylKit object.}
#'     \item{mean_mCpG}{The mean methylation percentage across CpGs in the methylKit object.}
#'   }
#'
#' @examples
#' # Load a methylKit object
#' mkRawObj <- methylKit::methRead("example_methylKit.txt")
#'
#' # Calculate methylation statistics
#' stats <- sample_meth_stats(mkRawObj)
#'
#' # Print the result
#' print(stats)
#'
#' @export
sample_meth_stats <- function(mkRawObj) {
  tibble(
    sample = methylKit::getSampleID(mkRawObj),
    n_CpGs = nrow(methylKit::getData(mkRawObj)),
    mean_mCpG = mean(methylKit::getData(mkRawObj)$numCs / methylKit::getData(mkRawObj)$coverage),
    mean_coverage = mean(methylKit::getData(mkRawObj)$coverage),
    median_coverage = median(methylKit::getData(mkRawObj)$coverage)
  )
}

#' Convert a MethylBase object to a tibble
#'
#' This function takes a MethylBase object, typically generated using the methylKit
#' package, and converts it into a tibble for easier data manipulation and analysis.
#'
#' @param mku_obj A MethylBase object containing DNA methylation data.
#'
#' @return A tibble containing the converted DNA methylation data.
#'
#' @import tidyr
#' @import dplyr
#' @importFrom methylKit getData
#' @export
#'
#' @examples
#' # Load the methylKit package and create a MethylBase object (mku_obj)
#' library(methylKit)
#' data(methylKit)
#' mku_obj <- MethyLBase(obj = methylKit.obj)
#'
#' # Convert the MethylBase object to a tibble
#' mku2tibble_result <- mku2tibble(mku_obj)
#' head(mku2tibble_result)
#'
#' @seealso
#' \code{\link{getData}} to retrieve data from a MethylBase object.
#'
#' @note
#' This function requires the methylKit, tidyr, and dplyr packages to be installed
#' and loaded.
#'
#' @references
#' Please refer to the methylKit package documentation for more information on
#' working with MethylBase objects.
#'
#' @author Your Name
#' @examples
#' # Load the methylKit package and create a MethylBase object (mku_obj)
#' library(methylKit)
#' data(methylKit)
#' mku_obj <- MethyLBase(obj = methylKit.obj)
#'
#' # Convert the MethylBase object to a tibble
#' mku2tibble_result <- mku2tibble(mku_obj)
#' head(mku2tibble_result)
#'
mku2tibble <- function(mku_obj) {
  suppressPackageStartupMessages(require(tidyr))
  suppressPackageStartupMessages(require(dplyr))

  sample_names <- mku_obj@sample.ids |>
    tibble::enframe(name = "sample_num", value = "sample")

  message(getwd())
  if ("dbpath" %in% slotNames(mku_obj)) {
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
