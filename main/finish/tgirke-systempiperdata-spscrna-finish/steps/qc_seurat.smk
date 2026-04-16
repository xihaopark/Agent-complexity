configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "qc_seurat"


rule all:
  input:
    "results/finish/qc_seurat.done"


rule run_qc_seurat:
  output:
    "results/finish/qc_seurat.done"
  run:
    run_step(STEP_ID, output[0])
