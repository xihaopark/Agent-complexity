configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calc_matrix_log2r_CSAW"


rule all:
  input:
    "results/finish/calc_matrix_log2r_CSAW.done"


rule run_calc_matrix_log2r_CSAW:
  output:
    "results/finish/calc_matrix_log2r_CSAW.done"
  run:
    run_step(STEP_ID, output[0])
