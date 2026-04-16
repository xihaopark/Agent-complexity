configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_umap_singlets_doublets"


rule all:
  input:
    "results/finish/plot_umap_singlets_doublets.done"


rule run_plot_umap_singlets_doublets:
  output:
    "results/finish/plot_umap_singlets_doublets.done"
  run:
    run_step(STEP_ID, output[0])
