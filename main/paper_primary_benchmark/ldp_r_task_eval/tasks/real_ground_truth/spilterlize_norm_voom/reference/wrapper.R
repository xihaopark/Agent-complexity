
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/spilterlize_norm_voom/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/spilterlize_norm_voom/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list(`filtered_counts` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/spilterlize_norm_voom/input/filtered_counts.csv"),
  output = list(`normalized_counts` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/spilterlize_norm_voom/reference_output/normalized_counts.csv", `voom_plot` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/spilterlize_norm_voom/reference_output/_voom.png"),
  params = list(`split` = "all"),
  wildcards = list(),
  config = list(`edgeR_parameters` = list(`refColumn` = "NULL", `logratioTrim` = 0.3, `sumTrim` = 0.05, `doWeighting` = "TRUE", `Acutoff` = -10000000000.0, `p` = 0.75), `voom_parameters` = list(`calcNormFactors_method` = "TMM", `normalize.method` = "none", `span` = 0.5)),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/spilterlize_norm_voom/reference"
)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
