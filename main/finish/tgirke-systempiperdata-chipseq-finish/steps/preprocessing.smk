configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "preprocessing"


rule all:
  input:
    "results/finish/preprocessing.done"


rule run_preprocessing:
  output:
    "results/finish/preprocessing.done"
  run:
    run_step(STEP_ID, output[0])
