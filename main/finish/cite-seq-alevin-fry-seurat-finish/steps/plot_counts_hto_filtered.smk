configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_counts_hto_filtered"


rule all:
  input:
    "results/finish/plot_counts_hto_filtered.done"


rule run_plot_counts_hto_filtered:
  output:
    "results/finish/plot_counts_hto_filtered.done"
  run:
    run_step(STEP_ID, output[0])
