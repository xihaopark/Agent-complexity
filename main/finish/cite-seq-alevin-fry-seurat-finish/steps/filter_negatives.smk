configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_negatives"


rule all:
  input:
    "results/finish/filter_negatives.done"


rule run_filter_negatives:
  output:
    "results/finish/filter_negatives.done"
  run:
    run_step(STEP_ID, output[0])
