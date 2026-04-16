configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter"


rule all:
  input:
    "results/finish/filter.done"


rule run_filter:
  output:
    "results/finish/filter.done"
  run:
    run_step(STEP_ID, output[0])
