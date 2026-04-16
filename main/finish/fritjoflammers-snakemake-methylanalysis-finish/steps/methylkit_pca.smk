configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_pca"


rule all:
  input:
    "results/finish/methylkit_pca.done"


rule run_methylkit_pca:
  output:
    "results/finish/methylkit_pca.done"
  run:
    run_step(STEP_ID, output[0])
