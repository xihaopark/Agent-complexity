configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_confidence_bed"


rule all:
  input:
    "results/finish/get_confidence_bed.done"


rule run_get_confidence_bed:
  output:
    "results/finish/get_confidence_bed.done"
  run:
    run_step(STEP_ID, output[0])
