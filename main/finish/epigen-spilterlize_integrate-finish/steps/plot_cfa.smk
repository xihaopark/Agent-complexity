configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_cfa"


rule all:
  input:
    "results/finish/plot_cfa.done"


rule run_plot_cfa:
  output:
    "results/finish/plot_cfa.done"
  run:
    run_step(STEP_ID, output[0])
