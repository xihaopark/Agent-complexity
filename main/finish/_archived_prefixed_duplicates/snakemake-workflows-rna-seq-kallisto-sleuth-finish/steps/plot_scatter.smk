configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_scatter"


rule all:
  input:
    "results/finish/plot_scatter.done"


rule run_plot_scatter:
  output:
    "results/finish/plot_scatter.done"
  run:
    run_step(STEP_ID, output[0])
