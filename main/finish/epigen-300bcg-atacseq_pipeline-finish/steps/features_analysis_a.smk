configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "features_analysis_a"


rule all:
  input:
    "results/finish/features_analysis_a.done"


rule run_features_analysis_a:
  output:
    "results/finish/features_analysis_a.done"
  run:
    run_step(STEP_ID, output[0])
