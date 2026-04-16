configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "validate_config"


rule all:
  input:
    "results/finish/validate_config.done"


rule run_validate_config:
  output:
    "results/finish/validate_config.done"
  run:
    run_step(STEP_ID, output[0])
