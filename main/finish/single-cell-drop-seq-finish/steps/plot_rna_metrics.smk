configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_rna_metrics"


rule all:
  input:
    "results/finish/plot_rna_metrics.done"


rule run_plot_rna_metrics:
  output:
    "results/finish/plot_rna_metrics.done"
  run:
    run_step(STEP_ID, output[0])
