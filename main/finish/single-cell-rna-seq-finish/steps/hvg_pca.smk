configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "hvg_pca"


rule all:
  input:
    "results/finish/hvg_pca.done"


rule run_hvg_pca:
  output:
    "results/finish/hvg_pca.done"
  run:
    run_step(STEP_ID, output[0])
