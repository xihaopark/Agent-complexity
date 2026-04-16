configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "trim"


rule all:
  input:
    "results/finish/trim.done"


rule run_trim:
  output:
    "results/finish/trim.done"
  run:
    run_step(STEP_ID, output[0])
