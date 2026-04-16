configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_truthsets"


rule all:
  input:
    "results/finish/merge_truthsets.done"


rule run_merge_truthsets:
  output:
    "results/finish/merge_truthsets.done"
  run:
    run_step(STEP_ID, output[0])
