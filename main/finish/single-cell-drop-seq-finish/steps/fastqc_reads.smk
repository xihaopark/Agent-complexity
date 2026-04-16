configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastqc_reads"


rule all:
  input:
    "results/finish/fastqc_reads.done"


rule run_fastqc_reads:
  output:
    "results/finish/fastqc_reads.done"
  run:
    run_step(STEP_ID, output[0])
