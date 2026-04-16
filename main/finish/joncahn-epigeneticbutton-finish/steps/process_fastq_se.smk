configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "process_fastq_se"


rule all:
  input:
    "results/finish/process_fastq_se.done"


rule run_process_fastq_se:
  output:
    "results/finish/process_fastq_se.done"
  run:
    run_step(STEP_ID, output[0])
