configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_filter_normalize"


rule all:
  input:
    "results/finish/methylkit_filter_normalize.done"


rule run_methylkit_filter_normalize:
  output:
    "results/finish/methylkit_filter_normalize.done"
  run:
    run_step(STEP_ID, output[0])
