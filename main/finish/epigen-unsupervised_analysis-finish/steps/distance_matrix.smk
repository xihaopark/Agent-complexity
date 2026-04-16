configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "distance_matrix"


rule all:
  input:
    "results/finish/distance_matrix.done"


rule run_distance_matrix:
  output:
    "results/finish/distance_matrix.done"
  run:
    run_step(STEP_ID, output[0])
