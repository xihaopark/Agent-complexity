configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_dimred_interactive"


rule all:
  input:
    "results/finish/plot_dimred_interactive.done"


rule run_plot_dimred_interactive:
  output:
    "results/finish/plot_dimred_interactive.done"
  run:
    run_step(STEP_ID, output[0])
