configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "uropa_prepare"


rule all:
  input:
    "results/finish/uropa_prepare.done"


rule run_uropa_prepare:
  output:
    "results/finish/uropa_prepare.done"
  run:
    run_step(STEP_ID, output[0])
