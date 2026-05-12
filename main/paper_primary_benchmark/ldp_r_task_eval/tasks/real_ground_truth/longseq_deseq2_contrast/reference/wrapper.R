
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/longseq_deseq2_contrast/input/dds.rds"),
  output = list(`table` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference_output/contrast_results.tsv", `ma_plot` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference_output/_ma.svg", `sample_heatmap` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference_output/_sample_heatmap.svg", `count_heatmap` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference_output/_count_heatmap.svg", `top_count_heatmap` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference_output/_top_count_heatmap.svg", `dispersion_plot` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference_output/_dispersion.svg"),
  params = list(`factor` = "condition", `prop_a` = "ko", `prop_b` = "wt", `alpha` = 0.05, `lfc_null` = 0.0, `alt_hypothesis` = "greaterAbs", `colormap` = "Blues", `threshold_plot` = 50),
  wildcards = list(),
  config = list(`deseq2` = list(`mincount` = 10)),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/longseq_deseq2_contrast/reference"
)

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
