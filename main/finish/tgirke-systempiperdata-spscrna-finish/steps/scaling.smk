configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "scaling"


rule all:
  input:
    "results/finish/scaling.done"


rule run_scaling:
  output:
    "results/finish/scaling.done"
  run:
    run_step(STEP_ID, output[0])
