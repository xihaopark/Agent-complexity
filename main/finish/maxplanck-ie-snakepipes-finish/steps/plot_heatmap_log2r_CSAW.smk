configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_heatmap_log2r_CSAW"


rule all:
  input:
    "results/finish/plot_heatmap_log2r_CSAW.done"


rule run_plot_heatmap_log2r_CSAW:
  output:
    "results/finish/plot_heatmap_log2r_CSAW.done"
  run:
    run_step(STEP_ID, output[0])
