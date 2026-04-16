configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotting_heatmap_on_targetfile"


rule all:
  input:
    "results/finish/plotting_heatmap_on_targetfile.done"


rule run_plotting_heatmap_on_targetfile:
  output:
    "results/finish/plotting_heatmap_on_targetfile.done"
  run:
    run_step(STEP_ID, output[0])
