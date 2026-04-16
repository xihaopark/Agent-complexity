configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_load"


rule all:
  input:
    "results/finish/methylkit_load.done"


rule run_methylkit_load:
  output:
    "results/finish/methylkit_load.done"
  run:
    run_step(STEP_ID, output[0])
