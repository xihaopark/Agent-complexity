configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "explorer"


rule all:
  input:
    "results/finish/explorer.done"


rule run_explorer:
  output:
    "results/finish/explorer.done"
  run:
    run_step(STEP_ID, output[0])
