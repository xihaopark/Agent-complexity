configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "microphaser_filter"


rule all:
  input:
    "results/finish/microphaser_filter.done"


rule run_microphaser_filter:
  output:
    "results/finish/microphaser_filter.done"
  run:
    run_step(STEP_ID, output[0])
