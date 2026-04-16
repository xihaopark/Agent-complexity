configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "making_stranded_matrix_on_targetfile"


rule all:
  input:
    "results/finish/making_stranded_matrix_on_targetfile.done"


rule run_making_stranded_matrix_on_targetfile:
  output:
    "results/finish/making_stranded_matrix_on_targetfile.done"
  run:
    run_step(STEP_ID, output[0])
