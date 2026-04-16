configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "violine_plots"


rule all:
  input:
    "results/finish/violine_plots.done"


rule run_violine_plots:
  output:
    "results/finish/violine_plots.done"
  run:
    run_step(STEP_ID, output[0])
