configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastqc"


rule all:
  input:
    "results/finish/fastqc.done"


rule run_fastqc:
  output:
    "results/finish/fastqc.done"
  run:
    run_step(STEP_ID, output[0])
