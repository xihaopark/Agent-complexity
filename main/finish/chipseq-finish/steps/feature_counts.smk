configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "feature_counts"


rule all:
  input:
    "results/finish/feature_counts.done"


rule run_feature_counts:
  output:
    "results/finish/feature_counts.done"
  run:
    run_step(STEP_ID, output[0])
