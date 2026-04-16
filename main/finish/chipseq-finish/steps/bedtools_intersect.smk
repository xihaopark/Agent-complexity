configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedtools_intersect"


rule all:
  input:
    "results/finish/bedtools_intersect.done"


rule run_bedtools_intersect:
  output:
    "results/finish/bedtools_intersect.done"
  run:
    run_step(STEP_ID, output[0])
