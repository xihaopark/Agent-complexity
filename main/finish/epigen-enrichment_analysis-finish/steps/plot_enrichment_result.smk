configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_enrichment_result"


rule all:
  input:
    "results/finish/plot_enrichment_result.done"


rule run_plot_enrichment_result:
  output:
    "results/finish/plot_enrichment_result.done"
  run:
    run_step(STEP_ID, output[0])
