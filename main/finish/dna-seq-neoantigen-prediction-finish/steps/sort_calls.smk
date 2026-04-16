configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort_calls"


rule all:
  input:
    "results/finish/sort_calls.done"


rule run_sort_calls:
  output:
    "results/finish/sort_calls.done"
  run:
    run_step(STEP_ID, output[0])
