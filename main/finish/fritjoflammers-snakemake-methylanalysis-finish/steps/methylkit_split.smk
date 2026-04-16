configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_split"


rule all:
  input:
    "results/finish/methylkit_split.done"


rule run_methylkit_split:
  output:
    "results/finish/methylkit_split.done"
  run:
    run_step(STEP_ID, output[0])
