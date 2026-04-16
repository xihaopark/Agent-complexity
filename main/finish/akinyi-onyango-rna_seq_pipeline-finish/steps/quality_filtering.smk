configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quality_filtering"


rule all:
  input:
    "results/finish/quality_filtering.done"


rule run_quality_filtering:
  output:
    "results/finish/quality_filtering.done"
  run:
    run_step(STEP_ID, output[0])
