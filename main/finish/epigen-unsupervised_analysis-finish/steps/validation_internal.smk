configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "validation_internal"


rule all:
  input:
    "results/finish/validation_internal.done"


rule run_validation_internal:
  output:
    "results/finish/validation_internal.done"
  run:
    run_step(STEP_ID, output[0])
