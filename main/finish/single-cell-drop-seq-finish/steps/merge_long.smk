configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_long"


rule all:
  input:
    "results/finish/merge_long.done"


rule run_merge_long:
  output:
    "results/finish/merge_long.done"
  run:
    run_step(STEP_ID, output[0])
