configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "OptiType"


rule all:
  input:
    "results/finish/OptiType.done"


rule run_OptiType:
  output:
    "results/finish/OptiType.done"
  run:
    run_step(STEP_ID, output[0])
