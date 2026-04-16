configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filtering"


rule all:
  input:
    "results/finish/filtering.done"


rule run_filtering:
  output:
    "results/finish/filtering.done"
  run:
    run_step(STEP_ID, output[0])
