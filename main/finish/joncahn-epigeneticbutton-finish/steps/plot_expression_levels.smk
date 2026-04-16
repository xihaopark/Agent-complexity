configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_expression_levels"


rule all:
  input:
    "results/finish/plot_expression_levels.done"


rule run_plot_expression_levels:
  output:
    "results/finish/plot_expression_levels.done"
  run:
    run_step(STEP_ID, output[0])
