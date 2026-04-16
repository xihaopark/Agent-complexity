configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "dimreduction"


rule all:
  input:
    "results/finish/dimreduction.done"


rule run_dimreduction:
  output:
    "results/finish/dimreduction.done"
  run:
    run_step(STEP_ID, output[0])
