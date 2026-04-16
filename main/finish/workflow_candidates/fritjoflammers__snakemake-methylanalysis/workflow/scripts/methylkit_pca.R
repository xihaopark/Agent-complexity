log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

# styler: off
INPUT_RDS                  <- snakemake@input$rds
METADATA_FILE              <- snakemake@input$sample_metadata
SPECIES_COLORS_FILE        <- snakemake@input$colors_file
SPECIES_METADATA_FILE      <- snakemake@input$species_metadata

OUTPUT_PLOT_PDF            <- snakemake@output$pca_plot
# styler: on

source(file.path(snakemake@scriptdir, "load_metadata.R"))
source(file.path(snakemake@scriptdir, "calc_pca.R"))

library(ggplot2)


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

mku <- readRDS(INPUT_RDS)

df_pca_variance <- calc_PCA(
  mku,
  metadata = METADATA,
  variance = T,
  impute = T
)

df_pca <- calc_PCA(
  mku,
  metadata = METADATA,
  impute = T
)

# PLOT PCA

screeplot <- df_pca_variance |>
  ggplot() +
  geom_line(aes(x = comp, y = var_explained)) +
  xlab("Principal Component") +
  ylab("Variance Explained") +
  ggtitle("Scree Plot") +
  ylim(0, 1)

pcaplot <- ggplot(
  df_pca,
  aes(x = PC1, y = PC2, color = Species)
) +
  geom_point(size = 2) +
  # ggrepel::geom_text_repel(aes(label=sample)) +
  # theme_minimal() +
  theme(legend.position = "none") +
  scale_color_manual(values = colors)

pcaplot_pc1long <- df_pca |>
  ggplot(aes(x = as.numeric(collection_longitude_dec), y = PC1, color = Species)) +
  geom_point() +
  # ggrepel::geom_text_repel(aes(label=sample)) +
  ggtitle("PC1 vs. Longitude") +
  theme(legend.position = "none") +
  scale_color_manual(values = colors) +
  xlab("Sampling Longitude")


pcaplot_pc2long <- df_pca |>
  ggplot(aes(x = as.numeric(collection_longitude_dec), y = PC2, color = Species)) +
  geom_point() +
  # ggrepel::geom_text_repel(aes(label=sample)) +
  ggtitle("PC2 vs. Longitude") +
  theme(legend.position = "none") +
  scale_color_manual(values = colors) +
  xlab("Sampling Longitude")



ggpubr::ggarrange(screeplot, pcaplot, pcaplot_pc1long, pcaplot_pc2long, common.legend = TRUE)

ggsave(OUTPUT_PLOT_PDF)
