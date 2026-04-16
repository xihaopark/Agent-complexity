configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_barnyard"


rule all:
  input:
    "results/finish/plot_barnyard.done"


rule run_plot_barnyard:
  output:
    "results/finish/plot_barnyard.done"
  run:
    run_step(STEP_ID, output[0])
