configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotation"


rule all:
  input:
    "results/finish/annotation.done"


rule run_annotation:
  output:
    "results/finish/annotation.done"
  run:
    run_step(STEP_ID, output[0])
