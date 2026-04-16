configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_knee_plot"


rule all:
  input:
    "results/finish/plot_knee_plot.done"


rule run_plot_knee_plot:
  output:
    "results/finish/plot_knee_plot.done"
  run:
    run_step(STEP_ID, output[0])
