configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "recalibrate_base_qualities"


rule all:
  input:
    "results/finish/recalibrate_base_qualities.done"


rule run_recalibrate_base_qualities:
  output:
    "results/finish/recalibrate_base_qualities.done"
  run:
    run_step(STEP_ID, output[0])
