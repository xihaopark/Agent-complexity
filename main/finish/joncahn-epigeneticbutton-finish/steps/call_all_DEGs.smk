configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_all_DEGs"


rule all:
  input:
    "results/finish/call_all_DEGs.done"


rule run_call_all_DEGs:
  output:
    "results/finish/call_all_DEGs.done"
  run:
    run_step(STEP_ID, output[0])
