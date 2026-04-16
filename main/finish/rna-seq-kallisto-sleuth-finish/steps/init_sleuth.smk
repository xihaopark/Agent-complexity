configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "init_sleuth"


rule all:
  input:
    "results/finish/init_sleuth.done"


rule run_init_sleuth:
  output:
    "results/finish/init_sleuth.done"
  run:
    run_step(STEP_ID, output[0])
