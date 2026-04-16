configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_pca"


rule all:
  input:
    "results/finish/plot_pca.done"


rule run_plot_pca:
  output:
    "results/finish/plot_pca.done"
  run:
    run_step(STEP_ID, output[0])
