configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "normalize"


rule all:
  input:
    "results/finish/normalize.done"


rule run_normalize:
  output:
    "results/finish/normalize.done"
  run:
    run_step(STEP_ID, output[0])
