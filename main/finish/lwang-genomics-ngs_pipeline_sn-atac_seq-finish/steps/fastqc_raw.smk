configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastqc_raw"


rule all:
  input:
    "results/finish/fastqc_raw.done"


rule run_fastqc_raw:
  output:
    "results/finish/fastqc_raw.done"
  run:
    run_step(STEP_ID, output[0])
