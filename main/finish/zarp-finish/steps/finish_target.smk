configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "finish_target"


rule all:
  input:
    "results/finish/finish_target.done"


rule run_finish_target:
  output:
    "results/finish/finish_target.done"
  run:
    run_step(STEP_ID, output[0])
