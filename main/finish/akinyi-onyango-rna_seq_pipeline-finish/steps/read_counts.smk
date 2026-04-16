configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "read_counts"


rule all:
  input:
    "results/finish/read_counts.done"


rule run_read_counts:
  output:
    "results/finish/read_counts.done"
  run:
    run_step(STEP_ID, output[0])
