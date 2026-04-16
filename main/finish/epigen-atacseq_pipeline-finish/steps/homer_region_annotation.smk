configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "homer_region_annotation"


rule all:
  input:
    "results/finish/homer_region_annotation.done"


rule run_homer_region_annotation:
  output:
    "results/finish/homer_region_annotation.done"
  run:
    run_step(STEP_ID, output[0])
