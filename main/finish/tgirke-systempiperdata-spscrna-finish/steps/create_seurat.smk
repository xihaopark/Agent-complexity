configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_seurat"


rule all:
  input:
    "results/finish/create_seurat.done"


rule run_create_seurat:
  output:
    "results/finish/create_seurat.done"
  run:
    run_step(STEP_ID, output[0])
