configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "env_export"


rule all:
  input:
    "results/finish/env_export.done"


rule run_env_export:
  output:
    "results/finish/env_export.done"
  run:
    run_step(STEP_ID, output[0])
