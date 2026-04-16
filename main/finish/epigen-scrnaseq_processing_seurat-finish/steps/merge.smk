configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge"


rule all:
  input:
    "results/finish/merge.done"


rule run_merge:
  output:
    "results/finish/merge.done"
  run:
    run_step(STEP_ID, output[0])
