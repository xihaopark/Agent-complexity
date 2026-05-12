
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/chipseq_plot_frip_score/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/chipseq_plot_frip_score/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/chipseq_plot_frip_score/input/sampleA_control.frip.txt", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/chipseq_plot_frip_score/input/sampleB_control.frip.txt", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/chipseq_plot_frip_score/input/sampleC_control.frip.txt", "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/chipseq_plot_frip_score/input/sampleD_control.frip.txt"),
  output = list(`1` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/chipseq_plot_frip_score/reference_output/_ignored.png"),
  params = list(),
  wildcards = list(),
  config = list(),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/chipseq_plot_frip_score/reference"
)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
# --- post-source hook -------------------------------------------------------

# Emit the tibble `frip_scores` (defined by the sourced script) as TSV.
readr::write_tsv(frip_scores, "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/chipseq_plot_frip_score/reference_output/frip_scores.tsv")

