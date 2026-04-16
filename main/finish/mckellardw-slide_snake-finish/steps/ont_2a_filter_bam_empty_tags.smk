configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_filter_bam_empty_tags"


rule all:
  input:
    "results/finish/ont_2a_filter_bam_empty_tags.done"


rule run_ont_2a_filter_bam_empty_tags:
  output:
    "results/finish/ont_2a_filter_bam_empty_tags.done"
  run:
    run_step(STEP_ID, output[0])
