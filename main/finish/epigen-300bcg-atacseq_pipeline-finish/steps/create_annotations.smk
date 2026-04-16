configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_annotations"


rule all:
  input:
    "results/finish/create_annotations.done"


rule run_create_annotations:
  output:
    "results/finish/create_annotations.done"
  run:
    run_step(STEP_ID, output[0])
