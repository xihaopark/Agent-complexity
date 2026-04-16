configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_call_adapter_scan"


rule all:
  input:
    "results/finish/ont_1a_call_adapter_scan.done"


rule run_ont_1a_call_adapter_scan:
  output:
    "results/finish/ont_1a_call_adapter_scan.done"
  run:
    run_step(STEP_ID, output[0])
