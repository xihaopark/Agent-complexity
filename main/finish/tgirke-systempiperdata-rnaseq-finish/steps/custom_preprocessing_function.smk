configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "custom_preprocessing_function"


rule all:
  input:
    "results/finish/custom_preprocessing_function.done"


rule run_custom_preprocessing_function:
  output:
    "results/finish/custom_preprocessing_function.done"
  run:
    run_step(STEP_ID, output[0])
