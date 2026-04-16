configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_refFlat"


rule all:
  input:
    "results/finish/create_refFlat.done"


rule run_create_refFlat:
  output:
    "results/finish/create_refFlat.done"
  run:
    run_step(STEP_ID, output[0])
