configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_split_bam_by_strand"


rule all:
  input:
    "results/finish/ont_2a_split_bam_by_strand.done"


rule run_ont_2a_split_bam_by_strand:
  output:
    "results/finish/ont_2a_split_bam_by_strand.done"
  run:
    run_step(STEP_ID, output[0])
