configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calling"


rule all:
  input:
    "results/finish/calling.done"


rule run_calling:
  output:
    "results/finish/calling.done"
  run:
    run_step(STEP_ID, output[0])
