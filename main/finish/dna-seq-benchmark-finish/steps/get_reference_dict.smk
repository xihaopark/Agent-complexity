configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_reference_dict"


rule all:
  input:
    "results/finish/get_reference_dict.done"


rule run_get_reference_dict:
  output:
    "results/finish/get_reference_dict.done"
  run:
    run_step(STEP_ID, output[0])
