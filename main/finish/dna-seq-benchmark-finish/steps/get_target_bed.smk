configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_target_bed"


rule all:
  input:
    "results/finish/get_target_bed.done"


rule run_get_target_bed:
  output:
    "results/finish/get_target_bed.done"
  run:
    run_step(STEP_ID, output[0])
