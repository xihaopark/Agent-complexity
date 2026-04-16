configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bowtie2_alignment"


rule all:
  input:
    "results/finish/bowtie2_alignment.done"


rule run_bowtie2_alignment:
  output:
    "results/finish/bowtie2_alignment.done"
  run:
    run_step(STEP_ID, output[0])
