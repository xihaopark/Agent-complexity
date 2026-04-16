configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_cellranger_multi_config_csv"


rule all:
  input:
    "results/finish/create_cellranger_multi_config_csv.done"


rule run_create_cellranger_multi_config_csv:
  output:
    "results/finish/create_cellranger_multi_config_csv.done"
  run:
    run_step(STEP_ID, output[0])
