configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_group_density"


rule all:
  input:
    "results/finish/plot_group_density.done"


rule run_plot_group_density:
  output:
    "results/finish/plot_group_density.done"
  run:
    run_step(STEP_ID, output[0])
