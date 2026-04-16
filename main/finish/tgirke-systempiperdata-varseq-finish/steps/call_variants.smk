configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_variants"


rule all:
  input:
    "results/finish/call_variants.done"


rule run_call_variants:
  output:
    "results/finish/call_variants.done"
  run:
    run_step(STEP_ID, output[0])
