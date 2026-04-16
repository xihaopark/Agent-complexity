configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "add_features"


rule all:
  input:
    "results/finish/add_features.done"


rule run_add_features:
  output:
    "results/finish/add_features.done"
  run:
    run_step(STEP_ID, output[0])
