configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_sum_annotatepeaks"


rule all:
  input:
    "results/finish/plot_sum_annotatepeaks.done"


rule run_plot_sum_annotatepeaks:
  output:
    "results/finish/plot_sum_annotatepeaks.done"
  run:
    run_step(STEP_ID, output[0])
