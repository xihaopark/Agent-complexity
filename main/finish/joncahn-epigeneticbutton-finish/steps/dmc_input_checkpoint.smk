configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "dmc_input_checkpoint"


rule all:
  input:
    "results/finish/dmc_input_checkpoint.done"


rule run_dmc_input_checkpoint:
  output:
    "results/finish/dmc_input_checkpoint.done"
  run:
    run_step(STEP_ID, output[0])
