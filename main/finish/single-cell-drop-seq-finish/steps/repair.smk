configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "repair"


rule all:
  input:
    "results/finish/repair.done"


rule run_repair:
  output:
    "results/finish/repair.done"
  run:
    run_step(STEP_ID, output[0])
