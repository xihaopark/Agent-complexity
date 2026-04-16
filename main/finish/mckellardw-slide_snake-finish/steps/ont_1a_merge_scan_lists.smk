configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_merge_scan_lists"


rule all:
  input:
    "results/finish/ont_1a_merge_scan_lists.done"


rule run_ont_1a_merge_scan_lists:
  output:
    "results/finish/ont_1a_merge_scan_lists.done"
  run:
    run_step(STEP_ID, output[0])
