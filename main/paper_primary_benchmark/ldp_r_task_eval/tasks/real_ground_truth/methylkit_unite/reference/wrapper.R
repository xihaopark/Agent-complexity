
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_unite/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_unite/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list("placeholder"),
  output = list(`rds` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_unite/reference_output/mk_united.rds", `stats_tsv` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_unite/reference_output/unite_stats.tsv", `db_file` = "output/_unite_db.txt.bgz"),
  params = list(`min_per_group` = 1, `destrand` = FALSE, `use_db` = FALSE),
  wildcards = list(),
  config = list(),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_unite/reference"
)

# --- pre-source hook --------------------------------------------------------

suppressPackageStartupMessages({
  library(methylKit)
})
# Upstream synthesis: load the per-sample bismark.cov files into a
# methylRawList via methRead, so the downstream unite() script can
# treat its input as a methylRawList exactly as the pipeline does.
mk_raw <- methylKit::methRead(
  location  = as.list(list("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_unite/input/sampleA.bismark.cov", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_unite/input/sampleB.bismark.cov", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_unite/input/sampleC.bismark.cov", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_unite/input/sampleD.bismark.cov")),
  sample.id = as.list(list("sampleA", "sampleB", "sampleC", "sampleD")),
  assembly  = "mock_v1",
  treatment = as.integer(c(0,0,1,1)),
  header    = FALSE,
  mincov    = 4,
  pipeline  = "bismarkCoverage"
)
mk_raw_rds <- file.path("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/methylkit_unite/input", "mk_raw.rds")
saveRDS(mk_raw, mk_raw_rds)
# Update snakemake@input[[1]] to point to this freshly-saved RDS.
snakemake@input <- list(mk_raw_rds)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
