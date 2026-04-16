configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "hvg_tsne"


rule all:
  input:
    "results/finish/hvg_tsne.done"


rule run_hvg_tsne:
  output:
    "results/finish/hvg_tsne.done"
  run:
    run_step(STEP_ID, output[0])
