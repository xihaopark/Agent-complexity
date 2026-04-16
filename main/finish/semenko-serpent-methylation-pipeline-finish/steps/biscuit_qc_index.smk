configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "biscuit_qc_index"


rule all:
  input:
    "results/finish/biscuit_qc_index.done"


rule run_biscuit_qc_index:
  output:
    "results/finish/biscuit_qc_index.done"
  run:
    run_step(STEP_ID, output[0])
