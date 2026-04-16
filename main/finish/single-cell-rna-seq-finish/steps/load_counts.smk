configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "load_counts"


rule all:
  input:
    "results/finish/load_counts.done"


rule run_load_counts:
  output:
    "results/finish/load_counts.done"
  run:
    run_step(STEP_ID, output[0])
