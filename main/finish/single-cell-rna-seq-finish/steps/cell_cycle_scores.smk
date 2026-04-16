configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cell_cycle_scores"


rule all:
  input:
    "results/finish/cell_cycle_scores.done"


rule run_cell_cycle_scores:
  output:
    "results/finish/cell_cycle_scores.done"
  run:
    run_step(STEP_ID, output[0])
