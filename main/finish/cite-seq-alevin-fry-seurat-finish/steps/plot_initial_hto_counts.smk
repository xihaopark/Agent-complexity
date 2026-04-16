configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_initial_hto_counts"


rule all:
  input:
    "results/finish/plot_initial_hto_counts.done"


rule run_plot_initial_hto_counts:
  output:
    "results/finish/plot_initial_hto_counts.done"
  run:
    run_step(STEP_ID, output[0])
