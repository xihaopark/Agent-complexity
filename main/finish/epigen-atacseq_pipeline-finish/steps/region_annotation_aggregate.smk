configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "region_annotation_aggregate"


rule all:
  input:
    "results/finish/region_annotation_aggregate.done"


rule run_region_annotation_aggregate:
  output:
    "results/finish/region_annotation_aggregate.done"
  run:
    run_step(STEP_ID, output[0])
