configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "stage_inputs"


rule all:
  input:
    "results/finish/stage_inputs.done"


rule run_stage_inputs:
  output:
    "results/finish/stage_inputs.done"
  run:
    run_step(STEP_ID, output[0])
