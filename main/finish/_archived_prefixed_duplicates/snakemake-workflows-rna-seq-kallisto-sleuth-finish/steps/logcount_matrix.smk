configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "logcount_matrix"


rule all:
  input:
    "results/finish/logcount_matrix.done"


rule run_logcount_matrix:
  output:
    "results/finish/logcount_matrix.done"
  run:
    run_step(STEP_ID, output[0])
