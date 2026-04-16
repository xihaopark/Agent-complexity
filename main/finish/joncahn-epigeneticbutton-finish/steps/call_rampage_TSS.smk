configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_rampage_TSS"


rule all:
  input:
    "results/finish/call_rampage_TSS.done"


rule run_call_rampage_TSS:
  output:
    "results/finish/call_rampage_TSS.done"
  run:
    run_step(STEP_ID, output[0])
