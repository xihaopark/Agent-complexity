configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_pipeline_input"


rule all:
  input:
    "results/finish/prepare_pipeline_input.done"


rule run_prepare_pipeline_input:
  output:
    "results/finish/prepare_pipeline_input.done"
  run:
    run_step(STEP_ID, output[0])
