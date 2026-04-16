df_annotate_repeats <- df |>
  annotate_regions(gr_repeats) |>
  annotate_regions(gr_repeats_flank) |>
  select(seqnames, sample, start, end, RepeatClass.x, RepeatClass.y, flank, metric, value) |>
  mutate(RepeatClass.x = as.character(RepeatClass.x)) |>
  mutate(RepeatClass.y = as.character(RepeatClass.y)) |>
  mutate(RepeatClass = if_else(RepeatClass.y == RepeatClass.x, RepeatClass.x, "mixed")) |>
  select(-RepeatClass.x, -RepeatClass.y) |>
  mutate(flank = if_else(is.na(flank), "no flank", flank))

df_annotate_repeats <-
  df_annotate_repeats |>
  mutate(RepeatClass = if_else(RepeatClass == "NULL", "no repeat", RepeatClass)) |>
  mutate(flank = if_else(RepeatClass == "no repeat", "no repeat", flank)) |>
  tidyr::separate(RepeatClass, into = c("RepeatClass", "RepeatFamily"), sep = "/") |>
  filter(!str_detect(RepeatClass, "\\?"))

metadata_columns <- c(metadata_columns, "RepeatClass", "RepeatFamily", "flank")

df <- df_annotate_repeats |>
  # filter(flank != "no_flank") |>
  unique() |>
  tidyr::pivot_wider(
    id_cols = c(seqnames, start, end, sample, RepeatClass, RepeatFamily, flank),
    names_from = "metric",
    values_from = "value"
  ) |>
  dplyr::mutate(numTs = coverage - numCs) |>
  dplyr::select(seqnames, start, end, sample, numCs, numTs, RepeatClass, RepeatFamily, flank) |>
  add_metadata() |>
  anti_join(exclusion_variants)

plot_species_correlation <- function(df, species1, species2) {
  df |>
    ggplot(aes(x = !!sym(species1), y = !!sym(species2))) +
    geom_bin2d(bins = 50) +
    scale_fill_continuous(type = "viridis", trans = "log10") +
    geom_smooth(method = "lm") +
    labs(title = paste(species1, "vs", species2, "CpG Correlation"))
}


df_wide <-
  df |>
  widen_data() |>
  add_metadata() |>
  anti_join(exclusion_variants)

calculate_mean_CpG <- function(df, ...) {
  df |>
    mutate(mCpG = numCs / (numCs + numTs)) |>
    group_by(seqnames, start, end, Species, ...) |>
    summarise(mean_CpG = mean(mCpG)) |>
    pivot_wider(
      id_cols = c(seqnames, start, end, ...),
      names_from = "Species",
      values_from = "mean_CpG"
    )
}

df_wide_mean_CpG <- calculate_mean_CpG(df_wide)


calc_species_correlation <- function(df_wide, species1, species2) {
  df_wide |>
    ungroup() |>
    dplyr::select(-c(seqnames, start, end)) |>
    corrr::correlate(method = "spearman") |>
    corrr::rearrange() |>
    corrr::shave()
}

plot_species_correlation(df_wide_mean_CpG, "O. melanoleuca", "O. pleschanka") + theme_classic()
plot_species_correlation(df_wide_mean_CpG, "O. melanoleuca", "O. hispanica")
plot_species_correlation(df_wide_mean_CpG, "O. melanoleuca", "O. melanoleuca x pleschanka")
plot_species_correlation(df_wide_mean_CpG, "O. pleschanka", "O. melanoleuca x pleschanka")

calc_species_correlation(df_wide_mean_CpG) |> corrr::rplot(print_cor = TRUE)

df_wide |>
  mutate(mCpG = numCs / (numCs + numTs)) |>
  group_by(Species) |>
  # summarise(mean_mCpG = mean(mCpG)) |>
  ggplot(aes(
    x = Species,
    y = mCpG
  )) +
  geom_boxplot()
