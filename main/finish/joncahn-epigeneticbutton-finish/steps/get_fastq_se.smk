configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_fastq_se"


rule all:
  input:
    "results/finish/get_fastq_se.done"


rule run_get_fastq_se:
  output:
    "results/finish/get_fastq_se.done"
  run:
    run_step(STEP_ID, output[0])
