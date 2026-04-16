configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "normalize_calls"


rule all:
  input:
    "results/finish/normalize_calls.done"


rule run_normalize_calls:
  output:
    "results/finish/normalize_calls.done"
  run:
    run_step(STEP_ID, output[0])
