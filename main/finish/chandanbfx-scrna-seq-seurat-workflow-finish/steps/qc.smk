configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "qc"


rule all:
  input:
    "results/finish/qc.done"


rule run_qc:
  output:
    "results/finish/qc.done"
  run:
    run_step(STEP_ID, output[0])
