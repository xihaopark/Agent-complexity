configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastp"


rule all:
  input:
    "results/finish/fastp.done"


rule run_fastp:
  output:
    "results/finish/fastp.done"
  run:
    run_step(STEP_ID, output[0])
