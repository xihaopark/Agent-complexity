configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_adapter_scan_summary"


rule all:
  input:
    "results/finish/ont_1a_adapter_scan_summary.done"


rule run_ont_1a_adapter_scan_summary:
  output:
    "results/finish/ont_1a_adapter_scan_summary.done"
  run:
    run_step(STEP_ID, output[0])
