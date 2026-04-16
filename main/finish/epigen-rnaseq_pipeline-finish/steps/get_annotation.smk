configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_annotation"


rule all:
  input:
    "results/finish/get_annotation.done"


rule run_get_annotation:
  output:
    "results/finish/get_annotation.done"
  run:
    run_step(STEP_ID, output[0])
