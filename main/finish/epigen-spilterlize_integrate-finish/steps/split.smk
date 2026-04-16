configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "split"


rule all:
  input:
    "results/finish/split.done"


rule run_split:
  output:
    "results/finish/split.done"
  run:
    run_step(STEP_ID, output[0])
