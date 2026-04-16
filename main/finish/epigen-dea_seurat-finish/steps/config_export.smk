configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "config_export"


rule all:
  input:
    "results/finish/config_export.done"


rule run_config_export:
  output:
    "results/finish/config_export.done"
  run:
    run_step(STEP_ID, output[0])
