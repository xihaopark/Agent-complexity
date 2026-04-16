configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "feature_lists"


rule all:
  input:
    "results/finish/feature_lists.done"


rule run_feature_lists:
  output:
    "results/finish/feature_lists.done"
  run:
    run_step(STEP_ID, output[0])
