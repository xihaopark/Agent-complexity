configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cellranger_multi_files_summaries"


rule all:
  input:
    "results/finish/cellranger_multi_files_summaries.done"


rule run_cellranger_multi_files_summaries:
  output:
    "results/finish/cellranger_multi_files_summaries.done"
  run:
    run_step(STEP_ID, output[0])
