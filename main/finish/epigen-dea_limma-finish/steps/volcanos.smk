configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "volcanos"


rule all:
  input:
    "results/finish/volcanos.done"


rule run_volcanos:
  output:
    "results/finish/volcanos.done"
  run:
    run_step(STEP_ID, output[0])
