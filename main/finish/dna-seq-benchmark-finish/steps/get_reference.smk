configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_reference"


rule all:
  input:
    "results/finish/get_reference.done"


rule run_get_reference:
  output:
    "results/finish/get_reference.done"
  run:
    run_step(STEP_ID, output[0])
