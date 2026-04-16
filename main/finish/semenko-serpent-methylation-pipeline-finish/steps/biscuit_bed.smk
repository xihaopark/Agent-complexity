configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "biscuit_bed"


rule all:
  input:
    "results/finish/biscuit_bed.done"


rule run_biscuit_bed:
  output:
    "results/finish/biscuit_bed.done"
  run:
    run_step(STEP_ID, output[0])
