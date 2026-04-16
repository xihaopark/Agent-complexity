configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1a_merge_formats"


rule all:
  input:
    "results/finish/ont_1a_merge_formats.done"


rule run_ont_1a_merge_formats:
  output:
    "results/finish/ont_1a_merge_formats.done"
  run:
    run_step(STEP_ID, output[0])
