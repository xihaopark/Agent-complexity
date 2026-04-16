configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "destrand_calls"


rule all:
  input:
    "results/finish/destrand_calls.done"


rule run_destrand_calls:
  output:
    "results/finish/destrand_calls.done"
  run:
    run_step(STEP_ID, output[0])
