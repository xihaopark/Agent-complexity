configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "salmon_alevin"


rule all:
  input:
    "results/finish/salmon_alevin.done"


rule run_salmon_alevin:
  output:
    "results/finish/salmon_alevin.done"
  run:
    run_step(STEP_ID, output[0])
