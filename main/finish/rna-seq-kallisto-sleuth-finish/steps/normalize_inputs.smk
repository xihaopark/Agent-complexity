configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "normalize_inputs"


rule all:
  input:
    "results/finish/normalize_inputs.done"


rule run_normalize_inputs:
  output:
    "results/finish/normalize_inputs.done"
  run:
    run_step(STEP_ID, output[0])
