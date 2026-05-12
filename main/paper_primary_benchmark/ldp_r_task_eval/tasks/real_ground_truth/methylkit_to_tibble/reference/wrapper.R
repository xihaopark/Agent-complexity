
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_to_tibble/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_to_tibble/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list(`rds` = "placeholder"),
  output = list(`rds` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_to_tibble/reference_output/df_mku.rds", `stats_tsv` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_to_tibble/reference_output/mean_mcpg.tsv"),
  params = list(),
  wildcards = list(),
  config = list(),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_to_tibble/reference"
)

# --- pre-source hook --------------------------------------------------------

suppressPackageStartupMessages({
  library(methylKit)
})
mk_raw <- methylKit::methRead(
  location  = as.list(list("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input/sampleA.bismark.cov", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input/sampleB.bismark.cov", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input/sampleC.bismark.cov", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input/sampleD.bismark.cov")),
  sample.id = as.list(list("sampleA", "sampleB", "sampleC", "sampleD")),
  assembly  = "mock_v1",
  treatment = as.integer(c(0,0,1,1)),
  header    = FALSE,
  mincov    = 4,
  pipeline  = "bismarkCoverage",
  dbtype    = "tabix",
  dbdir     = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input/mk_db"
)
mk_united <- methylKit::unite(
  mk_raw,
  min.per.group = 1L,
  destrand = FALSE,
  save.db = TRUE,
  dbdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input/mk_db",
  suffix = "unite"
)
mk_rds <- file.path("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_to_tibble/input", "mk_united.rds")
saveRDS(mk_united, mk_rds)
snakemake@input$rds <- mk_rds

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
