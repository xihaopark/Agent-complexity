configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "validation_external"


rule all:
  input:
    "results/finish/validation_external.done"


rule run_validation_external:
  output:
    "results/finish/validation_external.done"
  run:
    run_step(STEP_ID, output[0])
