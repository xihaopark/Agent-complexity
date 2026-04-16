configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sam_to_bam"


rule all:
  input:
    "results/finish/sam_to_bam.done"


rule run_sam_to_bam:
  output:
    "results/finish/sam_to_bam.done"
  run:
    run_step(STEP_ID, output[0])
