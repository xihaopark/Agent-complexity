configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_annotations"


rule all:
  input:
    "results/finish/merge_annotations.done"


rule run_merge_annotations:
  output:
    "results/finish/merge_annotations.done"
  run:
    run_step(STEP_ID, output[0])
