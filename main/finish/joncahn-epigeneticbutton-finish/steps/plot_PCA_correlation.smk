configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_PCA_correlation"


rule all:
  input:
    "results/finish/plot_PCA_correlation.done"


rule run_plot_PCA_correlation:
  output:
    "results/finish/plot_PCA_correlation.done"
  run:
    run_step(STEP_ID, output[0])
