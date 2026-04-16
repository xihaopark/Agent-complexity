configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastp_se"


rule all:
  input:
    "results/finish/fastp_se.done"


rule run_fastp_se:
  output:
    "results/finish/fastp_se.done"
  run:
    run_step(STEP_ID, output[0])
