configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fastqc_bam"


rule all:
  input:
    "results/finish/fastqc_bam.done"


rule run_fastqc_bam:
  output:
    "results/finish/fastqc_bam.done"
  run:
    run_step(STEP_ID, output[0])
