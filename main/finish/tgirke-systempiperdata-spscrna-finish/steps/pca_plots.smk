configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pca_plots"


rule all:
  input:
    "results/finish/pca_plots.done"


rule run_pca_plots:
  output:
    "results/finish/pca_plots.done"
  run:
    run_step(STEP_ID, output[0])
