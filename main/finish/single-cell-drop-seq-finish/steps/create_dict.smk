configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "create_dict"


rule all:
  input:
    "results/finish/create_dict.done"


rule run_create_dict:
  output:
    "results/finish/create_dict.done"
  run:
    run_step(STEP_ID, output[0])
