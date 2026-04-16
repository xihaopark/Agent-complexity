configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "split_annotation"


rule all:
  input:
    "results/finish/split_annotation.done"


rule run_split_annotation:
  output:
    "results/finish/split_annotation.done"
  run:
    run_step(STEP_ID, output[0])
