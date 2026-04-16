configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_unique"


rule all:
  input:
    "results/finish/filter_unique.done"


rule run_filter_unique:
  output:
    "results/finish/filter_unique.done"
  run:
    run_step(STEP_ID, output[0])
