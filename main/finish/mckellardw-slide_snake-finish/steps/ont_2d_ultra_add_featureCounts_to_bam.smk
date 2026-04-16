configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2d_ultra_add_featureCounts_to_bam"


rule all:
  input:
    "results/finish/ont_2d_ultra_add_featureCounts_to_bam.done"


rule run_ont_2d_ultra_add_featureCounts_to_bam:
  output:
    "results/finish/ont_2d_ultra_add_featureCounts_to_bam.done"
  run:
    run_step(STEP_ID, output[0])
