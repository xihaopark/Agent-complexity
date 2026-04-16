configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "trim_filter"


rule all:
  input:
    "results/finish/trim_filter.done"


rule run_trim_filter:
  output:
    "results/finish/trim_filter.done"
  run:
    run_step(STEP_ID, output[0])
