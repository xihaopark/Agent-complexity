configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedtools_merge_narrow"


rule all:
  input:
    "results/finish/bedtools_merge_narrow.done"


rule run_bedtools_merge_narrow:
  output:
    "results/finish/bedtools_merge_narrow.done"
  run:
    run_step(STEP_ID, output[0])
