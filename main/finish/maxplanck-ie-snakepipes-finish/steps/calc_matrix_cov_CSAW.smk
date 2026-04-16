configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calc_matrix_cov_CSAW"


rule all:
  input:
    "results/finish/calc_matrix_cov_CSAW.done"


rule run_calc_matrix_cov_CSAW:
  output:
    "results/finish/calc_matrix_cov_CSAW.done"
  run:
    run_step(STEP_ID, output[0])
