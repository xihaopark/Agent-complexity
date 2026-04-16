configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_umap_connectivity"


rule all:
  input:
    "results/finish/plot_umap_connectivity.done"


rule run_plot_umap_connectivity:
  output:
    "results/finish/plot_umap_connectivity.done"
  run:
    run_step(STEP_ID, output[0])
