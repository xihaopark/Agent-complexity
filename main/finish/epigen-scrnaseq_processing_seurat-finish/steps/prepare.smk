configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare"


rule all:
  input:
    "results/finish/prepare.done"


rule run_prepare:
  output:
    "results/finish/prepare.done"
  run:
    run_step(STEP_ID, output[0])
