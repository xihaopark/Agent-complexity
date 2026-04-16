configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sleuth_init"


rule all:
  input:
    "results/finish/sleuth_init.done"


rule run_sleuth_init:
  output:
    "results/finish/sleuth_init.done"
  run:
    run_step(STEP_ID, output[0])
