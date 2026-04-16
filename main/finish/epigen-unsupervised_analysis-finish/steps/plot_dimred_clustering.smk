configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_dimred_clustering"


rule all:
  input:
    "results/finish/plot_dimred_clustering.done"


rule run_plot_dimred_clustering:
  output:
    "results/finish/plot_dimred_clustering.done"
  run:
    run_step(STEP_ID, output[0])
