configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_fragment_length_dist"


rule all:
  input:
    "results/finish/plot_fragment_length_dist.done"


rule run_plot_fragment_length_dist:
  output:
    "results/finish/plot_fragment_length_dist.done"
  run:
    run_step(STEP_ID, output[0])
