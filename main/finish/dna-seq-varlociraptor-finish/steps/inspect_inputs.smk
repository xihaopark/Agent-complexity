configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "inspect_inputs"


rule all:
  input:
    "results/finish/inspect_inputs.done"


rule run_inspect_inputs:
  output:
    "results/finish/inspect_inputs.done"
  run:
    run_step(STEP_ID, output[0])
