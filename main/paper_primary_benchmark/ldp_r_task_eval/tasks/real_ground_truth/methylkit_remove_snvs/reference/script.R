log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")

source(file.path(snakemake@scriptdir, "methylkit_common.R"))

suppressPackageStartupMessages(library(here))
suppressPackageStartupMessages(library(methylKit))
suppressPackageStartupMessages(library(tidyverse))


INPUT_TIBBLE <- snakemake@input$tibble
EXCLUSION_VARIANTS <- snakemake@input$exclusion_variants_bedfile
OUTPUT_RDS <- snakemake@output$tibble
OUTPUT_STATS <- snakemake@output$stats_tsv


exclusion_variants <- read_tsv(
  EXCLUSION_VARIANTS,
  col_names = c("seqnames", "start", "end", "ref", "alt", "score")
) |>
  mutate(start = start + 1)

df_united <- readRDS(INPUT_TIBBLE)

df_united_excl <- df_united |>
  anti_join(exclusion_variants, by = c("chr" = "seqnames", "start" = "start"))


saveRDS(df_united_excl, OUTPUT_RDS)

tibble(
  dataset = c("united", "united_excl"),
  n_sites = c(nrow(df_united), nrow(df_united_excl))
) |>
  write_tsv(OUTPUT_STATS)
