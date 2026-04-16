configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "load_SPR"


rule all:
  input:
    "results/finish/load_SPR.done"


rule run_load_SPR:
  output:
    "results/finish/load_SPR.done"
  run:
    run_step(STEP_ID, output[0])
