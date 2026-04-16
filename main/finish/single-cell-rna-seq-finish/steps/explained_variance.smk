configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "explained_variance"


rule all:
  input:
    "results/finish/explained_variance.done"


rule run_explained_variance:
  output:
    "results/finish/explained_variance.done"
  run:
    run_step(STEP_ID, output[0])
