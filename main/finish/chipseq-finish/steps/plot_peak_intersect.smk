configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_peak_intersect"


rule all:
  input:
    "results/finish/plot_peak_intersect.done"


rule run_plot_peak_intersect:
  output:
    "results/finish/plot_peak_intersect.done"
  run:
    run_step(STEP_ID, output[0])
