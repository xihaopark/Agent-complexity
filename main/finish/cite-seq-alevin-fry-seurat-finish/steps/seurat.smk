configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "seurat"


rule all:
  input:
    "results/finish/seurat.done"


rule run_seurat:
  output:
    "results/finish/seurat.done"
  run:
    run_step(STEP_ID, output[0])
