
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/star_deseq2_init/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/star_deseq2_init/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list(`counts` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/star_deseq2_init/input/counts.tsv"),
  output = list("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/star_deseq2_init/reference_output/dds.rds", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/star_deseq2_init/reference_output/normalized_counts.tsv"),
  params = list(),
  wildcards = list(),
  config = list(`samples` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/star_deseq2_init/input/samples.tsv", `diffexp` = list(`variables_of_interest` = list(`condition` = list(`base_level` = "untreated")), `batch_effects` = list(""), `model` = "~condition")),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/star_deseq2_init/reference"
)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
