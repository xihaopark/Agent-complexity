configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_read_counts"


rule all:
  input:
    "results/finish/merge_read_counts.done"


rule run_merge_read_counts:
  output:
    "results/finish/merge_read_counts.done"
  run:
    run_step(STEP_ID, output[0])
