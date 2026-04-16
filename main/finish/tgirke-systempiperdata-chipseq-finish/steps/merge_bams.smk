configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_bams"


rule all:
  input:
    "results/finish/merge_bams.done"


rule run_merge_bams:
  output:
    "results/finish/merge_bams.done"
  run:
    run_step(STEP_ID, output[0])
