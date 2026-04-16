configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedtools_annotation"


rule all:
  input:
    "results/finish/bedtools_annotation.done"


rule run_bedtools_annotation:
  output:
    "results/finish/bedtools_annotation.done"
  run:
    run_step(STEP_ID, output[0])
