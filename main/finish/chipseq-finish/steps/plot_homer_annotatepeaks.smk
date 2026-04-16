configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_homer_annotatepeaks"


rule all:
  input:
    "results/finish/plot_homer_annotatepeaks.done"


rule run_plot_homer_annotatepeaks:
  output:
    "results/finish/plot_homer_annotatepeaks.done"
  run:
    run_step(STEP_ID, output[0])
