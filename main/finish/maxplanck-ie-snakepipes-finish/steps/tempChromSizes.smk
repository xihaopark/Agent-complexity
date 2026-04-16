configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tempChromSizes"


rule all:
  input:
    "results/finish/tempChromSizes.done"


rule run_tempChromSizes:
  output:
    "results/finish/tempChromSizes.done"
  run:
    run_step(STEP_ID, output[0])
