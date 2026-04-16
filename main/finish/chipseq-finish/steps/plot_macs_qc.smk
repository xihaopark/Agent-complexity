configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_macs_qc"


rule all:
  input:
    "results/finish/plot_macs_qc.done"


rule run_plot_macs_qc:
  output:
    "results/finish/plot_macs_qc.done"
  run:
    run_step(STEP_ID, output[0])
