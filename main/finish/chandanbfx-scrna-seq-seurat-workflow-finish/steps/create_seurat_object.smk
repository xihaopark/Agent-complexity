configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_seurat_object"


rule all:
  input:
    "results/finish/create_seurat_object.done"


rule run_create_seurat_object:
  output:
    "results/finish/create_seurat_object.done"
  run:
    run_step(STEP_ID, output[0])
