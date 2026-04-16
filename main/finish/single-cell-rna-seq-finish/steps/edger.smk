configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "edger"


rule all:
  input:
    "results/finish/edger.done"


rule run_edger:
  output:
    "results/finish/edger.done"
  run:
    run_step(STEP_ID, output[0])
