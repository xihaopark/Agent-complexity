configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_dmc_input"


rule all:
  input:
    "results/finish/get_dmc_input.done"


rule run_get_dmc_input:
  output:
    "results/finish/get_dmc_input.done"
  run:
    run_step(STEP_ID, output[0])
