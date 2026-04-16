configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "razers3"


rule all:
  input:
    "results/finish/razers3.done"


rule run_razers3:
  output:
    "results/finish/razers3.done"
  run:
    run_step(STEP_ID, output[0])
