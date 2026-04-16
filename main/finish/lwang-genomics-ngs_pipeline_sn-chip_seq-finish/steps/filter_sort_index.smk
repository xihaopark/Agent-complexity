configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_sort_index"


rule all:
  input:
    "results/finish/filter_sort_index.done"


rule run_filter_sort_index:
  output:
    "results/finish/filter_sort_index.done"
  run:
    run_step(STEP_ID, output[0])
