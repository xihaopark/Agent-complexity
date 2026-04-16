configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastp_pe"


rule all:
  input:
    "results/finish/fastp_pe.done"


rule run_fastp_pe:
  output:
    "results/finish/fastp_pe.done"
  run:
    run_step(STEP_ID, output[0])
