configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plot_adapter_content"


rule all:
  input:
    "results/finish/plot_adapter_content.done"


rule run_plot_adapter_content:
  output:
    "results/finish/plot_adapter_content.done"
  run:
    run_step(STEP_ID, output[0])
