configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "load_data"


rule all:
  input:
    "results/finish/load_data.done"


rule run_load_data:
  output:
    "results/finish/load_data.done"
  run:
    run_step(STEP_ID, output[0])
