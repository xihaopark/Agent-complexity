configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sample_annotation"


rule all:
  input:
    "results/finish/sample_annotation.done"


rule run_sample_annotation:
  output:
    "results/finish/sample_annotation.done"
  run:
    run_step(STEP_ID, output[0])
