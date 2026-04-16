configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "CSAW"


rule all:
  input:
    "results/finish/CSAW.done"


rule run_CSAW:
  output:
    "results/finish/CSAW.done"
  run:
    run_step(STEP_ID, output[0])
