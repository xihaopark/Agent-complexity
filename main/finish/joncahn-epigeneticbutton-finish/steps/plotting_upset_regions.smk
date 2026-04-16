configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotting_upset_regions"


rule all:
  input:
    "results/finish/plotting_upset_regions.done"


rule run_plotting_upset_regions:
  output:
    "results/finish/plotting_upset_regions.done"
  run:
    run_step(STEP_ID, output[0])
