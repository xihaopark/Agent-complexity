configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "features_analysis_b"


rule all:
  input:
    "results/finish/features_analysis_b.done"


rule run_features_analysis_b:
  output:
    "results/finish/features_analysis_b.done"
  run:
    run_step(STEP_ID, output[0])
