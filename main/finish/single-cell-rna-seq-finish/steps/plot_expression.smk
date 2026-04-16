configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_expression"


rule all:
  input:
    "results/finish/plot_expression.done"


rule run_plot_expression:
  output:
    "results/finish/plot_expression.done"
  run:
    run_step(STEP_ID, output[0])
