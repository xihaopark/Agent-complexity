configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_var_boxplot"


rule all:
  input:
    "results/finish/plot_var_boxplot.done"


rule run_plot_var_boxplot:
  output:
    "results/finish/plot_var_boxplot.done"
  run:
    run_step(STEP_ID, output[0])
