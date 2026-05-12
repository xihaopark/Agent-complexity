
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_filt_norm/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_filt_norm/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list("placeholder"),
  output = list(`rds` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_filt_norm/reference_output/mk_filt_norm.rds", `stats_tsv` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_filt_norm/reference_output/filt_norm_stats.tsv", `plots_filt` = "output/_plots_filt/.sentinel", `plots_norm` = "output/_plots_norm/.sentinel"),
  params = list(`low_cov_threshold_abs` = 3, `high_cov_threshold_perc` = 99.9),
  wildcards = list(),
  config = list(),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts"
)

# --- pre-source hook --------------------------------------------------------

suppressPackageStartupMessages({
  library(methylKit)
})
# Upstream: methRead to produce mk_raw, then save to input/mk_raw.rds so the
# filt_norm script's `readRDS(INPUT_FILE)` can consume it.
mk_raw <- methylKit::methRead(
  location  = as.list(list("input/sampleA.bismark.cov", "input/sampleB.bismark.cov", "input/sampleC.bismark.cov")),
  sample.id = as.list(list("sampleA", "sampleB", "sampleC")),
  assembly  = "mock_v1",
  treatment = as.integer(c(0,0,1)),
  header    = FALSE, mincov = 4, pipeline = "bismarkCoverage"
)
mk_raw_rds <- "input/mk_raw.rds"
saveRDS(mk_raw, mk_raw_rds)
snakemake@input <- list(mk_raw_rds)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
