configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_reference"


rule all:
  input:
    "results/finish/prepare_reference.done"


rule run_prepare_reference:
  output:
    "results/finish/prepare_reference.done"
  run:
    run_step(STEP_ID, output[0])
