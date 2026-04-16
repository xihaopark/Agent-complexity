configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merging_matrix"


rule all:
  input:
    "results/finish/merging_matrix.done"


rule run_merging_matrix:
  output:
    "results/finish/merging_matrix.done"
  run:
    run_step(STEP_ID, output[0])
