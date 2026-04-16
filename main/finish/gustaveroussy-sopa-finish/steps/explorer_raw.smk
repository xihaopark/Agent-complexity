configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "explorer_raw"


rule all:
  input:
    "results/finish/explorer_raw.done"


rule run_explorer_raw:
  output:
    "results/finish/explorer_raw.done"
  run:
    run_step(STEP_ID, output[0])
