configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mapping"


rule all:
  input:
    "results/finish/mapping.done"


rule run_mapping:
  output:
    "results/finish/mapping.done"
  run:
    run_step(STEP_ID, output[0])
