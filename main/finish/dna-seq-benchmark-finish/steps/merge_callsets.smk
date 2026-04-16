configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_callsets"


rule all:
  input:
    "results/finish/merge_callsets.done"


rule run_merge_callsets:
  output:
    "results/finish/merge_callsets.done"
  run:
    run_step(STEP_ID, output[0])
