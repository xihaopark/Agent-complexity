configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "volcano"


rule all:
  input:
    "results/finish/volcano.done"


rule run_volcano:
  output:
    "results/finish/volcano.done"
  run:
    run_step(STEP_ID, output[0])
