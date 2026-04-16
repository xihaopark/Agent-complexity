configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_unit_bams_per_sample"


rule all:
  input:
    "results/finish/merge_unit_bams_per_sample.done"


rule run_merge_unit_bams_per_sample:
  output:
    "results/finish/merge_unit_bams_per_sample.done"
  run:
    run_step(STEP_ID, output[0])
