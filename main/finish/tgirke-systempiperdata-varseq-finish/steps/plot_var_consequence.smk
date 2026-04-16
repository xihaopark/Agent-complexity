configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_var_consequence"


rule all:
  input:
    "results/finish/plot_var_consequence.done"


rule run_plot_var_consequence:
  output:
    "results/finish/plot_var_consequence.done"
  run:
    run_step(STEP_ID, output[0])
