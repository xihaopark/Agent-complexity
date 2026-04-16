configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_3_bam"


rule all:
  input:
    "results/finish/ont_3a_readQC_3_bam.done"


rule run_ont_3a_readQC_3_bam:
  output:
    "results/finish/ont_3a_readQC_3_bam.done"
  run:
    run_step(STEP_ID, output[0])
