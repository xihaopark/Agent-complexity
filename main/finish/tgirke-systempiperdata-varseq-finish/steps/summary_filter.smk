configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "summary_filter"


rule all:
  input:
    "results/finish/summary_filter.done"


rule run_summary_filter:
  output:
    "results/finish/summary_filter.done"
  run:
    run_step(STEP_ID, output[0])
