configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_calls"


rule all:
  input:
    "results/finish/merge_calls.done"


rule run_merge_calls:
  output:
    "results/finish/merge_calls.done"
  run:
    run_step(STEP_ID, output[0])
