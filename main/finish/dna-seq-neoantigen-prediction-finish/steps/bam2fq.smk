configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam2fq"


rule all:
  input:
    "results/finish/bam2fq.done"


rule run_bam2fq:
  output:
    "results/finish/bam2fq.done"
  run:
    run_step(STEP_ID, output[0])
