configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_cellranger_library_csv"


rule all:
  input:
    "results/finish/create_cellranger_library_csv.done"


rule run_create_cellranger_library_csv:
  output:
    "results/finish/create_cellranger_library_csv.done"
  run:
    run_step(STEP_ID, output[0])
