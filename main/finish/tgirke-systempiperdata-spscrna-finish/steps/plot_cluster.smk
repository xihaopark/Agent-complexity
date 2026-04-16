configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_cluster"


rule all:
  input:
    "results/finish/plot_cluster.done"


rule run_plot_cluster:
  output:
    "results/finish/plot_cluster.done"
  run:
    run_step(STEP_ID, output[0])
