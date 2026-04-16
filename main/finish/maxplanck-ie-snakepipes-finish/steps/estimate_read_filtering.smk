configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "estimate_read_filtering"


rule all:
  input:
    "results/finish/estimate_read_filtering.done"


rule run_estimate_read_filtering:
  output:
    "results/finish/estimate_read_filtering.done"
  run:
    run_step(STEP_ID, output[0])
