configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedtools_merge_broad"


rule all:
  input:
    "results/finish/bedtools_merge_broad.done"


rule run_bedtools_merge_broad:
  output:
    "results/finish/bedtools_merge_broad.done"
  run:
    run_step(STEP_ID, output[0])
