configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_dimred_metadata"


rule all:
  input:
    "results/finish/plot_dimred_metadata.done"


rule run_plot_dimred_metadata:
  output:
    "results/finish/plot_dimred_metadata.done"
  run:
    run_step(STEP_ID, output[0])
