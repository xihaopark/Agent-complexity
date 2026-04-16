configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "feature_counting"


rule all:
  input:
    "results/finish/feature_counting.done"


rule run_feature_counting:
  output:
    "results/finish/feature_counting.done"
  run:
    run_step(STEP_ID, output[0])
