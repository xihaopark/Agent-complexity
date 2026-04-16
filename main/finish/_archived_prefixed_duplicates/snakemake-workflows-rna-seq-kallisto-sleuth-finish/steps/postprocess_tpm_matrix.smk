configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "postprocess_tpm_matrix"


rule all:
  input:
    "results/finish/postprocess_tpm_matrix.done"


rule run_postprocess_tpm_matrix:
  output:
    "results/finish/postprocess_tpm_matrix.done"
  run:
    run_step(STEP_ID, output[0])
