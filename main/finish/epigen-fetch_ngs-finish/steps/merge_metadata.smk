configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_metadata"


rule all:
  input:
    "results/finish/merge_metadata.done"


rule run_merge_metadata:
  output:
    "results/finish/merge_metadata.done"
  run:
    run_step(STEP_ID, output[0])
