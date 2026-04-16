configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_chip"


rule all:
  input:
    "results/finish/all_chip.done"


rule run_all_chip:
  output:
    "results/finish/all_chip.done"
  run:
    run_step(STEP_ID, output[0])
