configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_available_bam"


rule all:
  input:
    "results/finish/get_available_bam.done"


rule run_get_available_bam:
  output:
    "results/finish/get_available_bam.done"
  run:
    run_step(STEP_ID, output[0])
