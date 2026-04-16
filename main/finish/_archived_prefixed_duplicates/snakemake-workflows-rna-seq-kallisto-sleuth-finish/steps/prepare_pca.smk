configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_pca"


rule all:
  input:
    "results/finish/prepare_pca.done"


rule run_prepare_pca:
  output:
    "results/finish/prepare_pca.done"
  run:
    run_step(STEP_ID, output[0])
