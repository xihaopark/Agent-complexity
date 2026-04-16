configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calculate_coding_potential"


rule all:
  input:
    "results/finish/calculate_coding_potential.done"


rule run_calculate_coding_potential:
  output:
    "results/finish/calculate_coding_potential.done"
  run:
    run_step(STEP_ID, output[0])
