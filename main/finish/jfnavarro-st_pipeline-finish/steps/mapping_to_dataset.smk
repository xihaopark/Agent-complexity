configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mapping_to_dataset"


rule all:
  input:
    "results/finish/mapping_to_dataset.done"


rule run_mapping_to_dataset:
  output:
    "results/finish/mapping_to_dataset.done"
  run:
    run_step(STEP_ID, output[0])
