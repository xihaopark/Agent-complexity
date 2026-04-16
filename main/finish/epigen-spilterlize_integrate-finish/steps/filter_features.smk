configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_features"


rule all:
  input:
    "results/finish/filter_features.done"


rule run_filter_features:
  output:
    "results/finish/filter_features.done"
  run:
    run_step(STEP_ID, output[0])
