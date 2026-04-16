configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_cellassign"


rule all:
  input:
    "results/finish/plot_cellassign.done"


rule run_plot_cellassign:
  output:
    "results/finish/plot_cellassign.done"
  run:
    run_step(STEP_ID, output[0])
