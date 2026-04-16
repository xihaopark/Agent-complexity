configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "concatenate_beds"


rule all:
  input:
    "results/finish/concatenate_beds.done"


rule run_concatenate_beds:
  output:
    "results/finish/concatenate_beds.done"
  run:
    run_step(STEP_ID, output[0])
