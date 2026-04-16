configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "uropa_reg"


rule all:
  input:
    "results/finish/uropa_reg.done"


rule run_uropa_reg:
  output:
    "results/finish/uropa_reg.done"
  run:
    run_step(STEP_ID, output[0])
