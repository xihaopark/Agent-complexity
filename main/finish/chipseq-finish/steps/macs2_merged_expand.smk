configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "macs2_merged_expand"


rule all:
  input:
    "results/finish/macs2_merged_expand.done"


rule run_macs2_merged_expand:
  output:
    "results/finish/macs2_merged_expand.done"
  run:
    run_step(STEP_ID, output[0])
