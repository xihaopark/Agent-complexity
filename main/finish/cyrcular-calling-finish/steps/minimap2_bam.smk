configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "minimap2_bam"


rule all:
  input:
    "results/finish/minimap2_bam.done"


rule run_minimap2_bam:
  output:
    "results/finish/minimap2_bam.done"
  run:
    run_step(STEP_ID, output[0])
