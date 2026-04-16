configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastq_to_bam"


rule all:
  input:
    "results/finish/fastq_to_bam.done"


rule run_fastq_to_bam:
  output:
    "results/finish/fastq_to_bam.done"
  run:
    run_step(STEP_ID, output[0])
