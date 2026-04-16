configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_cell_whitelist"


rule all:
  input:
    "results/finish/get_cell_whitelist.done"


rule run_get_cell_whitelist:
  output:
    "results/finish/get_cell_whitelist.done"
  run:
    run_step(STEP_ID, output[0])
