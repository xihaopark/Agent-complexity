configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "count_matrix"


rule all:
  input:
    "results/finish/count_matrix.done"


rule run_count_matrix:
  output:
    "results/finish/count_matrix.done"
  run:
    run_step(STEP_ID, output[0])
