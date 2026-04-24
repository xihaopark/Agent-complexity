
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

SCRIPT_TO_SOURCE <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_remove_snvs/reference/script.R"
LOG_PATH <- "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_remove_snvs/reference/run.R.log"
snakemake <- new(
  "SnakemakeMock",
  input = list(`tibble` = "placeholder", `exclusion_variants_bedfile` = "placeholder"),
  output = list(`tibble` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_remove_snvs/reference_output/df_united_excl.rds", `stats_tsv` = "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/methylkit_remove_snvs/reference_output/snv_stats.tsv"),
  params = list(),
  wildcards = list(),
  config = list(),
  threads = 1,
  log = list(LOG_PATH),
  scriptdir = "/Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts"
)

# --- pre-source hook --------------------------------------------------------

suppressPackageStartupMessages({
  library(methylKit); library(tidyverse)
})
source(file.path("/Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/scripts", "methylkit_common.R"))
files <- Sys.glob(file.path("input", "*.bismark.cov"))
sample_ids <- sub("\\.bismark\\.cov$", "", basename(files))
mk_raw <- methylKit::methRead(
  location = as.list(files), sample.id = as.list(sample_ids),
  assembly = "mock_v1",
  treatment = as.integer(seq_along(sample_ids) > length(sample_ids)/2),
  header = FALSE, mincov = 4, pipeline = "bismarkCoverage",
  dbtype = "tabix", dbdir = "input/mk_db"
)
mk_u <- methylKit::unite(mk_raw, min.per.group = 1L, destrand = FALSE,
                         save.db = TRUE, dbdir = "input/mk_db",
                         suffix = "unite")
df_united <- mku2tibble(mk_u)
saveRDS(df_united, "input/df_united.rds")
snakemake@input$tibble <- "input/df_united.rds"
snakemake@input$exclusion_variants_bedfile <- "input/exclusion.bed"

# --- source original script ------------------------------------------------
source(SCRIPT_TO_SOURCE, echo = FALSE, keep.source = TRUE)
