configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_rna_metrics_species"


rule all:
  input:
    "results/finish/plot_rna_metrics_species.done"


rule run_plot_rna_metrics_species:
  output:
    "results/finish/plot_rna_metrics_species.done"
  run:
    run_step(STEP_ID, output[0])
