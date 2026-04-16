configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sort"


rule all:
  input:
    "results/finish/sort.done"


rule run_sort:
  output:
    "results/finish/sort.done"
  run:
    run_step(STEP_ID, output[0])
