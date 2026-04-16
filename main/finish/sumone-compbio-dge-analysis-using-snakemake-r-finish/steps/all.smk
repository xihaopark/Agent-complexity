configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all"


rule all:
  input:
    "results/finish/all.done"


rule run_all:
  output:
    "results/finish/all.done"
  run:
    run_step(STEP_ID, output[0])
