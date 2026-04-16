configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gzip_fastq"


rule all:
  input:
    "results/finish/gzip_fastq.done"


rule run_gzip_fastq:
  output:
    "results/finish/gzip_fastq.done"
  run:
    run_step(STEP_ID, output[0])
