configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastq_report"


rule all:
  input:
    "results/finish/fastq_report.done"


rule run_fastq_report:
  output:
    "results/finish/fastq_report.done"
  run:
    run_step(STEP_ID, output[0])
