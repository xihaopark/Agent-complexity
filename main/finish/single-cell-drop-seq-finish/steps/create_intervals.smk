configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_intervals"


rule all:
  input:
    "results/finish/create_intervals.done"


rule run_create_intervals:
  output:
    "results/finish/create_intervals.done"
  run:
    run_step(STEP_ID, output[0])
