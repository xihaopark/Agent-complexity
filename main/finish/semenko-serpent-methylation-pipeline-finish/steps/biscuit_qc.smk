configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "biscuit_qc"


rule all:
  input:
    "results/finish/biscuit_qc.done"


rule run_biscuit_qc:
  output:
    "results/finish/biscuit_qc.done"
  run:
    run_step(STEP_ID, output[0])
