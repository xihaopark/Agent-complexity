configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_diagnostics"


rule all:
  input:
    "results/finish/plot_diagnostics.done"


rule run_plot_diagnostics:
  output:
    "results/finish/plot_diagnostics.done"
  run:
    run_step(STEP_ID, output[0])
