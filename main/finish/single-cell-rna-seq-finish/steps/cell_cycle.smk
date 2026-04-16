configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cell_cycle"


rule all:
  input:
    "results/finish/cell_cycle.done"


rule run_cell_cycle:
  output:
    "results/finish/cell_cycle.done"
  run:
    run_step(STEP_ID, output[0])
