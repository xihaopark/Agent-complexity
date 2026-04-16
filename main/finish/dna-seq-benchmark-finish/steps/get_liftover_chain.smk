configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_liftover_chain"


rule all:
  input:
    "results/finish/get_liftover_chain.done"


rule run_get_liftover_chain:
  output:
    "results/finish/get_liftover_chain.done"
  run:
    run_step(STEP_ID, output[0])
