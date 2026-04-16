configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_markers"


rule all:
  input:
    "results/finish/plot_markers.done"


rule run_plot_markers:
  output:
    "results/finish/plot_markers.done"
  run:
    run_step(STEP_ID, output[0])
