configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "computing_matrix_scales"


rule all:
  input:
    "results/finish/computing_matrix_scales.done"


rule run_computing_matrix_scales:
  output:
    "results/finish/computing_matrix_scales.done"
  run:
    run_step(STEP_ID, output[0])
