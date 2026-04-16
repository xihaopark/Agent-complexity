configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "feature_list_export"


rule all:
  input:
    "results/finish/feature_list_export.done"


rule run_feature_list_export:
  output:
    "results/finish/feature_list_export.done"
  run:
    run_step(STEP_ID, output[0])
