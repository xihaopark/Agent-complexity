log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

INPUT_FILE <- snakemake@input$df
METADATA_FILE <- snakemake@input$sample_metadata
SPECIES_COLORS_FILE <- snakemake@input$colors_file
SPECIES_METADATA_FILE <- snakemake@input$species_metadata
OUTPUT_CLUSTER_CIRCULAR <- snakemake@output$clustering_circular

#' Cluster Samples based on Methylation Data
#'
#' This function clusters samples based on methylation data using hierarchical clustering.
#'
#' @param df_mku A data frame containing methylation data with the following columns:
#'   - metric: A character vector indicating the type of metric (e.g., "coverage", "numCs", "numTs").
#'   - value: A numeric vector representing the corresponding metric values.
#'   - sample: A character vector containing the sample names.
#'   - chr: A character vector indicating the chromosome information.
#'   - start: A numeric vector representing the start position of the data.
#' @param .method A character string specifying the agglomeration method used in hierarchical clustering.
#'   The default value is "ward.D".
#' @return A dendrogram data object that can be used for plotting hierarchical cluster dendrograms.
#'
#' @import dplyr
#' @import tidyr
#' @import corrr
#' @import ggdendro
#'
#' @examples
#' # Assuming df_mku is a data frame with methylation data
#' cluster_results <- cluster_samples(df_mku, .method = "ward.D")
#' plot_cluster(cluster_results)
#'
#' @export
cluster_samples <- function(df_mku, .method = "ward.D") {
  df_mku_hc <-
    df_mku |>
    dplyr::select(metric, value, sample, chr, start) |>
    tidyr::pivot_wider(names_from = "metric", values_from = "value") |>
    dplyr::mutate(across(c("coverage", "numCs"), as.integer))

  dist.cor <- df_mku_hc |>
    dplyr::filter(!is.na(sample)) |>
    dplyr::mutate(
      mCpG = numCs / coverage,
      pos = paste0(chr, ".", start),
      sample = sample,
      .keep = "none"
    ) |>
    tidyr::pivot_wider(names_from = "sample", values_from = "mCpG") |>
    corrr::correlate(diagonal = 1)


  # get matrix with 1-distances
  m.dist.cor <- 1 - dist.cor |>
    dplyr::select(-term) |>
    data.matrix() |>
    as.dist()

  hc <- hclust(m.dist.cor, method = .method)
  hc.dendro <- as.dendrogram(hc)
  hc.dendrodata <- ggdendro::dendro_data(hc.dendro, type = "rectangle")

  return(hc.dendrodata)
}


#' Plot a Dendrogram of Hierarchical Clustering
#'
#' This function plots a dendrogram of hierarchical clustering.
#'
#' @param dendrodata A dendrogram data object obtained from the `cluster_samples` function.
#' @return A ggplot object representing the dendrogram plot.
#'
#' @import dplyr
#' @import ggdendro
#'
#' @examples
#' # Assuming cluster_data is the result of cluster_samples function
#' plot_cluster(cluster_data)
#'
#' @export
plot_cluster <- function(dendrodata, point_size = 1) {
  require(ggplot2)
  require(ggdendro)

  ggplot2::ggplot(ggdendro::segment(dendrodata)) +
    ggplot2::geom_segment(aes(x = x, y = y, xend = xend, yend = yend)) +
    ggplot2::coord_flip() +
    ggplot2::scale_y_reverse(expand = c(0.2, 0)) +
    ggdendro::theme_dendro() +
    # geom_text(data = hc.dendrodata$label,
    #            aes(label=label, x=x, y=-.1, color=Species), hjust=0) +
    ggplot2::geom_point(
      data = dendrodata$label,
      aes(x = x, y = -0, color = Species), size = point_size
    )
}


source(file.path(snakemake@scriptdir, "load_metadata.R"))

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

df_mku <- readRDS(INPUT_FILE)

hc.dendrodata <- cluster_samples(df_mku)

hc.dendrodata$label <-
  hc.dendrodata$label |>
  dplyr::left_join(METADATA, by = c("label" = "sample"))

plot_cluster(hc.dendrodata, point_size = 4) +
  ggplot2::scale_color_manual(values = colors) +
  ggplot2::coord_polar(direction = -1) +
  ggplot2::scale_x_continuous(
    breaks = NULL,
    limits = c(0, nrow(hc.dendrodata$label))
  )

ggplot2::ggsave(OUTPUT_CLUSTER_CIRCULAR)
