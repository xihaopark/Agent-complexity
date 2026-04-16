configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_annotations_for_bedfile"


rule all:
  input:
    "results/finish/get_annotations_for_bedfile.done"


rule run_get_annotations_for_bedfile:
  output:
    "results/finish/get_annotations_for_bedfile.done"
  run:
    run_step(STEP_ID, output[0])
