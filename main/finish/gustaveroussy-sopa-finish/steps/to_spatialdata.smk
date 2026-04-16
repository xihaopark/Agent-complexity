configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "to_spatialdata"


rule all:
  input:
    "results/finish/to_spatialdata.done"


rule run_to_spatialdata:
  output:
    "results/finish/to_spatialdata.done"
  run:
    run_step(STEP_ID, output[0])
