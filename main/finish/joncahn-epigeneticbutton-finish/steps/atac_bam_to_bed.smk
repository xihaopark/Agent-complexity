configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "atac_bam_to_bed"


rule all:
  input:
    "results/finish/atac_bam_to_bed.done"


rule run_atac_bam_to_bed:
  output:
    "results/finish/atac_bam_to_bed.done"
  run:
    run_step(STEP_ID, output[0])
