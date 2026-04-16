configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "flair_plot_isoforms"


rule all:
  input:
    "results/finish/flair_plot_isoforms.done"


rule run_flair_plot_isoforms:
  output:
    "results/finish/flair_plot_isoforms.done"
  run:
    run_step(STEP_ID, output[0])
