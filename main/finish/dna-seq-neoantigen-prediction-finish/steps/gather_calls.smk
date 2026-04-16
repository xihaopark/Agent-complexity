configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gather_calls"


rule all:
  input:
    "results/finish/gather_calls.done"


rule run_gather_calls:
  output:
    "results/finish/gather_calls.done"
  run:
    run_step(STEP_ID, output[0])
