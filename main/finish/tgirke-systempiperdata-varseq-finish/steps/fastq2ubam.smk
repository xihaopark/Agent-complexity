configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastq2ubam"


rule all:
  input:
    "results/finish/fastq2ubam.done"


rule run_fastq2ubam:
  output:
    "results/finish/fastq2ubam.done"
  run:
    run_step(STEP_ID, output[0])
