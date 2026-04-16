configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "read_mapping"


rule all:
  input:
    "results/finish/read_mapping.done"


rule run_read_mapping:
  output:
    "results/finish/read_mapping.done"
  run:
    run_step(STEP_ID, output[0])
