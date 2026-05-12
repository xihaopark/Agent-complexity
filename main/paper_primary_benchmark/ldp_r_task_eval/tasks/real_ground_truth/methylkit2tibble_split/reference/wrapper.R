
# --- SnakemakeMock preamble ---------------------------------------------------
# Minimal S4 stand-in for Snakemake's `snakemake` object so we can `source()`
# a Snakemake-authored R script outside any Snakemake context.
suppressPackageStartupMessages({
  if (!isClass("SnakemakeMock")) {
    setClass(
      "SnakemakeMock",
      representation(
        input = "list", output = "list", params = "list",
        wildcards = "list", config = "list", threads = "numeric",
        log = "list", scriptdir = "character", rule = "character",
        resources = "list"
      ),
      prototype(
        input = list(), output = list(), params = list(),
        wildcards = list(), config = list(), threads = 1,
        log = list(), scriptdir = ".", rule = "mock_rule",
        resources = list()
      )
    )
  }
})

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit2tibble_split/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit2tibble_split/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list(`rds_list` = list("placeholder")),
  output = list(`rds` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit2tibble_split/reference_output/df_mku_split.rds", `stats_tsv` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit2tibble_split/reference_output/mean_mcpg_split.tsv"),
  params = list(),
  wildcards = list(),
  config = list(),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts"
)

# --- pre-source hook --------------------------------------------------------

setwd("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit2tibble_split")
suppressPackageStartupMessages({
  library(methylKit); library(tidyverse)
})
group_to_rds <- list()
for (group in c("grp1","grp2")) {
  files <- Sys.glob(file.path("input", paste0(group, "__*.bismark.cov")))
  sample_ids <- sub("\\.bismark\\.cov$", "", basename(files))
  sample_ids <- sub(paste0("^", group, "__"), "", sample_ids)
  mk_raw <- methylKit::methRead(
    location  = as.list(files), sample.id = as.list(sample_ids),
    assembly = "mock_v1",
    treatment = as.integer(seq_along(sample_ids) > length(sample_ids) / 2),
    header = FALSE, mincov = 4, pipeline = "bismarkCoverage"
  )
  mk_u <- methylKit::unite(mk_raw, min.per.group = 1L, destrand = FALSE)
  out <- file.path("input", paste0(group, "_mku.rds"))
  saveRDS(mk_u, out)
  group_to_rds[[group]] <- out
}
snakemake@input$rds_list <- unlist(group_to_rds, use.names = FALSE)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
