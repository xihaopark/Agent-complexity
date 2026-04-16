configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "qc_trim"


rule all:
  input:
    "results/finish/qc_trim.done"


rule run_qc_trim:
  output:
    "results/finish/qc_trim.done"
  run:
    run_step(STEP_ID, output[0])
