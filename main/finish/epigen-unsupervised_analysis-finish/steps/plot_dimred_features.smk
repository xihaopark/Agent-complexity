configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_dimred_features"


rule all:
  input:
    "results/finish/plot_dimred_features.done"


rule run_plot_dimred_features:
  output:
    "results/finish/plot_dimred_features.done"
  run:
    run_step(STEP_ID, output[0])
