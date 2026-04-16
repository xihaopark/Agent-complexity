configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cellranger_count"


rule all:
  input:
    "results/finish/cellranger_count.done"


rule run_cellranger_count:
  output:
    "results/finish/cellranger_count.done"
  run:
    run_step(STEP_ID, output[0])
