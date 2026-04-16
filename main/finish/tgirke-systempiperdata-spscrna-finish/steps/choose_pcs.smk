configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "choose_pcs"


rule all:
  input:
    "results/finish/choose_pcs.done"


rule run_choose_pcs:
  output:
    "results/finish/choose_pcs.done"
  run:
    run_step(STEP_ID, output[0])
