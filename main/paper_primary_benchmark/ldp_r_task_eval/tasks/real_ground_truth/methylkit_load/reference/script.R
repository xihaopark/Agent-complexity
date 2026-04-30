log <- file(snakemake@log[[1]], open = "wt")
sink(log, type = "message")


library(here)
library(methylKit)
library(tidyverse)

message("loading methylkit")

source(file.path(snakemake@scriptdir, "methylkit_common.R"))

message(".. functions loaded.")
# styler: off
INPUT_FILES         <- as.list(snakemake@input)
SAMPLE_NAMES        <- as.list(snakemake@params$samples)
MIN_COV             <- snakemake@params$min_cov
ASSEMBLY_NAME       <- snakemake@params$assembly_name
CALLING_TOOL        <- snakemake@params$calling_tool
OUTPUT_RDS          <- snakemake@output$rds
OUTPUT_PLOTS        <- dirname(snakemake@output$plots)
#OUTPUT_MTH_PLOTS    <- snakemake@output$methylation_plots

# styler: on
TREATMENT <- as.integer(rep(0, length(SAMPLE_NAMES)))

message(".. starting methylKit...")

# set methRead pipeline to load files from
# bismark or methyldacke
if (CALLING_TOOL == "bismark") {
  pipeline_label <- "bismarkCoverage"
  with_header <- FALSE
} else if (CALLING_TOOL == "methyldackel") {
  pipeline_label <- "amp"
  with_header <- TRUE
}

message("using pipeline: ", pipeline_label)


mk_raw <- methylKit::methRead(
  location = INPUT_FILES,
  sample.id = SAMPLE_NAMES,
  assembly = ASSEMBLY_NAME,
  header = with_header,
  treatment = TREATMENT,
  mincov = MIN_COV,
  pipeline = pipeline_label
)

message("done!")

saveRDS(mk_raw, OUTPUT_RDS)

message(" ... start plots ...")

message("done!")
sink(NULL)
