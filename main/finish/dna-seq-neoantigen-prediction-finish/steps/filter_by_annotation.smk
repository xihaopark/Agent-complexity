configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_by_annotation"


rule all:
  input:
    "results/finish/filter_by_annotation.done"


rule run_filter_by_annotation:
  output:
    "results/finish/filter_by_annotation.done"
  run:
    run_step(STEP_ID, output[0])
