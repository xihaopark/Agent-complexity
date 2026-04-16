configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "seurat_plots"


rule all:
  input:
    "results/finish/seurat_plots.done"


rule run_seurat_plots:
  output:
    "results/finish/seurat_plots.done"
  run:
    run_step(STEP_ID, output[0])
