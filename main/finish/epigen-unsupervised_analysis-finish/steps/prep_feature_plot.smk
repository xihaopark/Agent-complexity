configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_feature_plot"


rule all:
  input:
    "results/finish/prep_feature_plot.done"


rule run_prep_feature_plot:
  output:
    "results/finish/prep_feature_plot.done"
  run:
    run_step(STEP_ID, output[0])
