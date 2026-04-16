configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cellranger_multi_run"


rule all:
  input:
    "results/finish/cellranger_multi_run.done"


rule run_cellranger_multi_run:
  output:
    "results/finish/cellranger_multi_run.done"
  run:
    run_step(STEP_ID, output[0])
