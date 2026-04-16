configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_profile"


rule all:
  input:
    "results/finish/plot_profile.done"


rule run_plot_profile:
  output:
    "results/finish/plot_profile.done"
  run:
    run_step(STEP_ID, output[0])
