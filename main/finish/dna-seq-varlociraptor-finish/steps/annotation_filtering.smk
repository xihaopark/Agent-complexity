configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotation_filtering"


rule all:
  input:
    "results/finish/annotation_filtering.done"


rule run_annotation_filtering:
  output:
    "results/finish/annotation_filtering.done"
  run:
    run_step(STEP_ID, output[0])
