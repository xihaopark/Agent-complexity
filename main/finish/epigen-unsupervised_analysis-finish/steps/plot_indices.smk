configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_indices"


rule all:
  input:
    "results/finish/plot_indices.done"


rule run_plot_indices:
  output:
    "results/finish/plot_indices.done"
  run:
    run_step(STEP_ID, output[0])
