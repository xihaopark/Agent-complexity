configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepare_references"


rule all:
  input:
    "results/finish/prepare_references.done"


rule run_prepare_references:
  output:
    "results/finish/prepare_references.done"
  run:
    run_step(STEP_ID, output[0])
