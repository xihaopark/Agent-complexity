configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "process_fastq_pe"


rule all:
  input:
    "results/finish/process_fastq_pe.done"


rule run_process_fastq_pe:
  output:
    "results/finish/process_fastq_pe.done"
  run:
    run_step(STEP_ID, output[0])
