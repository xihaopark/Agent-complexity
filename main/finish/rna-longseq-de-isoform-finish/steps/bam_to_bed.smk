configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_to_bed"


rule all:
  input:
    "results/finish/bam_to_bed.done"


rule run_bam_to_bed:
  output:
    "results/finish/bam_to_bed.done"
  run:
    run_step(STEP_ID, output[0])
