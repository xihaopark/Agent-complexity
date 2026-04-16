configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_split_fastq_to_R1_R2"


rule all:
  input:
    "results/finish/ont_1a_split_fastq_to_R1_R2.done"


rule run_ont_1a_split_fastq_to_R1_R2:
  output:
    "results/finish/ont_1a_split_fastq_to_R1_R2.done"
  run:
    run_step(STEP_ID, output[0])
