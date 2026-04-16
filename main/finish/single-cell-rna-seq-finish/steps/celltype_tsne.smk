configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "celltype_tsne"


rule all:
  input:
    "results/finish/celltype_tsne.done"


rule run_celltype_tsne:
  output:
    "results/finish/celltype_tsne.done"
  run:
    run_step(STEP_ID, output[0])
