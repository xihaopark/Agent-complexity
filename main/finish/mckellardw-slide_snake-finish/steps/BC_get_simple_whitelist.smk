configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "BC_get_simple_whitelist"


rule all:
  input:
    "results/finish/BC_get_simple_whitelist.done"


rule run_BC_get_simple_whitelist:
  output:
    "results/finish/BC_get_simple_whitelist.done"
  run:
    run_step(STEP_ID, output[0])
