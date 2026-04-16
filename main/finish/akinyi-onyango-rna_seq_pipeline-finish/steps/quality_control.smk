configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quality_control"


rule all:
  input:
    "results/finish/quality_control.done"


rule run_quality_control:
  output:
    "results/finish/quality_control.done"
  run:
    run_step(STEP_ID, output[0])
