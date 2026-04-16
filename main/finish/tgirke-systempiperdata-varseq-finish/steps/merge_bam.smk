configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_bam"


rule all:
  input:
    "results/finish/merge_bam.done"


rule run_merge_bam:
  output:
    "results/finish/merge_bam.done"
  run:
    run_step(STEP_ID, output[0])
