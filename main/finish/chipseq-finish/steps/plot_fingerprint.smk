configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_fingerprint"


rule all:
  input:
    "results/finish/plot_fingerprint.done"


rule run_plot_fingerprint:
  output:
    "results/finish/plot_fingerprint.done"
  run:
    run_step(STEP_ID, output[0])
