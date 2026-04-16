configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_vars"


rule all:
  input:
    "results/finish/plot_vars.done"


rule run_plot_vars:
  output:
    "results/finish/plot_vars.done"
  run:
    run_step(STEP_ID, output[0])
