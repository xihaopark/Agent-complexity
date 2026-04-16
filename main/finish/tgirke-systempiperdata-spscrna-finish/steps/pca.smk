configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pca"


rule all:
  input:
    "results/finish/pca.done"


rule run_pca:
  output:
    "results/finish/pca.done"
  run:
    run_step(STEP_ID, output[0])
