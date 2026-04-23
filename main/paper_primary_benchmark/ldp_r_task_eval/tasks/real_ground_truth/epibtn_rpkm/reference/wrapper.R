setwd("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/epibtn_rpkm/reference_output")
commandArgs <- function(trailingOnly = FALSE) if (trailingOnly) c(
  "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/epibtn_rpkm/input/genecount.tsv",
  "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/epibtn_rpkm/input/targets.tsv",
  "runX",
  "mockref",
  "/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real/epibtn_rpkm/input/ref_genes.bed"
) else c("Rscript")
source("/Users/park/code/Paper2Skills-main/main/paper_primary_benchmark/ldp_r_task_eval/tasks/real_ground_truth/epibtn_rpkm/reference/script.R", echo = FALSE)
