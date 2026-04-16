configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "store_config"


rule all:
  input:
    "results/finish/store_config.done"


rule run_store_config:
  output:
    "results/finish/store_config.done"
  run:
    run_step(STEP_ID, output[0])
