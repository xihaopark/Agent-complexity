configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_qc"


rule all:
  input:
    "results/finish/all_qc.done"


rule run_all_qc:
  output:
    "results/finish/all_qc.done"
  run:
    run_step(STEP_ID, output[0])
