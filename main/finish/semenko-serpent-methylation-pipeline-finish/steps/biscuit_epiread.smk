configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "biscuit_epiread"


rule all:
  input:
    "results/finish/biscuit_epiread.done"


rule run_biscuit_epiread:
  output:
    "results/finish/biscuit_epiread.done"
  run:
    run_step(STEP_ID, output[0])
