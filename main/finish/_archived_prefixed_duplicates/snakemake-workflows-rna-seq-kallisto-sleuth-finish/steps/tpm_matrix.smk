configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tpm_matrix"


rule all:
  input:
    "results/finish/tpm_matrix.done"


rule run_tpm_matrix:
  output:
    "results/finish/tpm_matrix.done"
  run:
    run_step(STEP_ID, output[0])
