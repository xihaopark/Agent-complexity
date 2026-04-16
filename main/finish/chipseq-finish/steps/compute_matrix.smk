configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "compute_matrix"


rule all:
  input:
    "results/finish/compute_matrix.done"


rule run_compute_matrix:
  output:
    "results/finish/compute_matrix.done"
  run:
    run_step(STEP_ID, output[0])
