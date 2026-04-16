configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "hvg"


rule all:
  input:
    "results/finish/hvg.done"


rule run_hvg:
  output:
    "results/finish/hvg.done"
  run:
    run_step(STEP_ID, output[0])
