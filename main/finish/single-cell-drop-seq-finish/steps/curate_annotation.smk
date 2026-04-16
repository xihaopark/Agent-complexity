configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "curate_annotation"


rule all:
  input:
    "results/finish/curate_annotation.done"


rule run_curate_annotation:
  output:
    "results/finish/curate_annotation.done"
  run:
    run_step(STEP_ID, output[0])
