configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_cells"


rule all:
  input:
    "results/finish/filter_cells.done"


rule run_filter_cells:
  output:
    "results/finish/filter_cells.done"
  run:
    run_step(STEP_ID, output[0])
