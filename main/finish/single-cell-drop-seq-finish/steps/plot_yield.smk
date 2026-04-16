configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_yield"


rule all:
  input:
    "results/finish/plot_yield.done"


rule run_plot_yield:
  output:
    "results/finish/plot_yield.done"
  run:
    run_step(STEP_ID, output[0])
