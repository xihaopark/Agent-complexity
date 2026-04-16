configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_paired_to_fastq"


rule all:
  input:
    "results/finish/bam_paired_to_fastq.done"


rule run_bam_paired_to_fastq:
  output:
    "results/finish/bam_paired_to_fastq.done"
  run:
    run_step(STEP_ID, output[0])
