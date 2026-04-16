configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "run_fastqc"


rule all:
  input:
    "results/finish/run_fastqc.done"


rule run_run_fastqc:
  output:
    "results/finish/run_fastqc.done"
  run:
    run_step(STEP_ID, output[0])
