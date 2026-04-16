configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_bootstrap"


rule all:
  input:
    "results/finish/plot_bootstrap.done"


rule run_plot_bootstrap:
  output:
    "results/finish/plot_bootstrap.done"
  run:
    run_step(STEP_ID, output[0])
