configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "run_edger"


rule all:
  input:
    "results/finish/run_edger.done"


rule run_run_edger:
  output:
    "results/finish/run_edger.done"
  run:
    run_step(STEP_ID, output[0])
