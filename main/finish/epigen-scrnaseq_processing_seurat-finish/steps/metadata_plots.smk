configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "metadata_plots"


rule all:
  input:
    "results/finish/metadata_plots.done"


rule run_metadata_plots:
  output:
    "results/finish/metadata_plots.done"
  run:
    run_step(STEP_ID, output[0])
