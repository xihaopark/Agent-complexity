configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_empty_file"


rule all:
  input:
    "results/finish/create_empty_file.done"


rule run_create_empty_file:
  output:
    "results/finish/create_empty_file.done"
  run:
    run_step(STEP_ID, output[0])
