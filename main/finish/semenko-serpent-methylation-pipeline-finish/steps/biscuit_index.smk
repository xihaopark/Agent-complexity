configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "biscuit_index"


rule all:
  input:
    "results/finish/biscuit_index.done"


rule run_biscuit_index:
  output:
    "results/finish/biscuit_index.done"
  run:
    run_step(STEP_ID, output[0])
