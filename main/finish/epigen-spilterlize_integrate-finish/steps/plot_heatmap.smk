configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_heatmap"


rule all:
  input:
    "results/finish/plot_heatmap.done"


rule run_plot_heatmap:
  output:
    "results/finish/plot_heatmap.done"
  run:
    run_step(STEP_ID, output[0])
