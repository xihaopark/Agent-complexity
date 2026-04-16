configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_sample_annotation"


rule all:
  input:
    "results/finish/plot_sample_annotation.done"


rule run_plot_sample_annotation:
  output:
    "results/finish/plot_sample_annotation.done"
  run:
    run_step(STEP_ID, output[0])
