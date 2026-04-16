configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_enrichment_scatter"


rule all:
  input:
    "results/finish/plot_enrichment_scatter.done"


rule run_plot_enrichment_scatter:
  output:
    "results/finish/plot_enrichment_scatter.done"
  run:
    run_step(STEP_ID, output[0])
