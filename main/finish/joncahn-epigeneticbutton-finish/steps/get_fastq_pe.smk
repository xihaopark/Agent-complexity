configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_fastq_pe"


rule all:
  input:
    "results/finish/get_fastq_pe.done"


rule run_get_fastq_pe:
  output:
    "results/finish/get_fastq_pe.done"
  run:
    run_step(STEP_ID, output[0])
